---
layout: ../../layouts/ContentLayout.astro
title: "TTS 발음은 텍스트가 아니라 전처리가 결정한다 — tts-sentence-preprocessor를 만든 이유"
date: 2026-08-07
tags: ["Voice AI", "AI Engineering"]
description: "Korean/English TTS를 위한 커스텀 텍스트 정규화·phonemization(IPA) 전처리 레포"
---

저장소

- [GitHub: jhwanseok/tts-sentence-preprocessor](https://github.com/jhwanseok/tts-sentence-preprocessor)

# "모델은 잘 학습됐는데, 왜 이렇게 어색하게 읽지?"

TTS 서비스를 운영하다 보면 이런 순간이 온다. 음성 모델 자체는 충분히 좋다. 그런데도 결과물을 들어보면 어딘가 어색하다. 숫자가 이상하게 읽히고, 약어가 알파벳 그대로 스펠링되고, 한국어 문장인데 발음이 뭉개진 것처럼 들린다. 처음에는 모델을 의심했다. 파인튜닝 데이터를 늘리고, 보코더를 바꿔보고, 하이퍼파라미터를 조정했다. 그런데 원인은 다른 곳에 있었다. <mark>모델에 들어가기 전, 텍스트가 "어떻게 읽어야 하는가"로 바뀌는 그 단계가 발음 품질의 상당 부분을 이미 결정하고 있었다.</mark>

`"1,200원"`을 모델이 직접 보고 "천이백 원"이라고 읽어주길 기대할 수는 없다. `"GPU"`를 "지피유"로 읽을지 "그래픽 처리 장치"로 풀어 읽을지도 모델이 알아서 정할 문제가 아니다. 이런 판단은 텍스트 전처리 단계에서 명시적으로 결정해야 하는 것이고, 서비스마다 요구사항이 다르다. 어떤 서비스는 "010-1234-5678"을 한 자리씩 읽어야 하고, 어떤 서비스는 통계 리포트처럼 숫자를 자연스러운 어절 단위로 읽어야 한다. 문제는 이런 규칙들이 실제 서비스 코드 안에서 뒤섞여 있으면, 새로운 규칙을 추가하거나 순서를 바꾸는 일이 점점 더 무서워진다는 것이었다.

> 발음이 이상한 건 모델 탓이 아니라, 텍스트를 "말할 수 있는 형태"로 바꾸는 전처리가 부실했기 때문이다.

`tts-sentence-preprocessor`는 이 판단들을 서비스 코드에서 분리해, 정규화(normalization)와 phonemization(발음 변환)을 독립적으로 관리하고 커스터마이징할 수 있게 만들기 위해 시작한 레포다. 이 글은 그 과정에서 마주친 설계 결정 두 가지 — 정규화 파이프라인을 어떻게 갈아 끼울 수 있게 만들었는지, 그리고 발음의 핵심이라 할 수 있는 <abbr title="International Phonetic Alphabet, 언어에 무관하게 실제 발음을 표기하는 국제 음성 기호 체계" tabindex="0">IPA</abbr> 변환에서 한국어와 영어를 왜 다르게 다뤄야 했는지 — 를 중심으로 정리한다.

---

# 정규화 파이프라인을 마음대로 갈아 끼울 수 있어야 했다

실제 서비스를 운영하다 보면 정규화 규칙은 계속 바뀐다. 새로운 도메인(예: 주소, 의료 용어)이 추가되면 규칙이 늘어나고, 두 규칙이 충돌하면 순서를 바꿔야 하고, 특정 서비스에만 필요한 예외는 공통 로직을 건드리지 않고 얹을 수 있어야 한다. 이 요구를 만족시키기 위해 `normalizer/base.py`의 `BaseNormalizer`는 정규화를 하나의 큰 함수가 아니라, **순서가 있는 변환 함수 리스트를 순차적으로 적용하는 fold 연산**으로 설계했다.

```python
class BaseNormalizer(ABC):
    def __init__(self) -> None:
        self.transforms = []

    def normalize(self, text: str, debug: bool = False) -> str:
        return reduce(lambda x, y: y(x, debug), self.transforms, text)
```

`normalize()` 자체는 아주 단순하다. `self.transforms`에 담긴 `(text, debug) -> text` 형태의 함수들을 `functools.reduce`로 순서대로 텍스트에 적용할 뿐이다. 설계의 핵심은 이 리스트를 어떻게 채우는지에 있다. `BaseNormalizer`는 ABC(추상 클래스)로, 공백 정리·유니코드 치환·특수문자 제거처럼 언어에 상관없이 재사용 가능한 단계는 `@staticmethod`로 미리 제공하고, 어휘 치환·숫자 읽기·특수 케이스 처리처럼 언어별로 반드시 달라지는 단계는 `@abstractmethod`로 비워둔다. `KoreanNormalizer`, `EnglishNormalizer` 같은 구체 클래스는 `init_transforms()`에서 이 둘을 조합해 파이프라인을 조립한다.

```python
class KoreanNormalizer(BaseNormalizer):
    def init_transforms(self) -> None:
        self.transforms += self.remove_consonants_vowels()  # 공통 단계
        self.transforms += self.collapse_whitespace()        # 공통 단계
        self.transforms += self.replace_voca()                # 언어별: 어휘 치환
        self.transforms += self.read_special_case()           # 언어별: 통화·단위·전화번호 등
        self.transforms += self.read_number()                  # 언어별: 숫자 읽기
        # ...
```

이 구조가 실제로 관리를 수월하게 만드는 지점은 세 가지다.

첫째, 순서는 이 메서드 안의 코드 순서 그 자체이므로, 단계를 추가하거나 빼거나 순서를 바꾸는 일이 `+=` 한 줄을 옮기는 문제로 줄어든다. 별도의 우선순위 숫자나 레지스트리를 관리할 필요가 없다.

둘째, 공통 단계와 언어별 단계가 명확히 분리돼 있어서, `KoreanEnglishNormalizer`처럼 두 언어가 섞인 문장을 처리해야 하는 경우에도 각 언어의 규칙 빌더 함수를 그대로 재사용할 수 있다.

셋째, `self.transforms`는 평범한 public 리스트이기 때문에, 서브클래스를 새로 만들지 않고도 인스턴스 생성 후 특정 서비스에서만 필요한 함수를 얹거나 빼는 것이 가능하다.

언어별 규칙(통화, 단위, 날짜, 전화번호, 약어 등)의 실제 치환 테이블은 코드가 아니라 `data/korean/`, `data/english/` 아래 CSV 파일로 관리한다. `_utils.py`의 `load_dict()`가 디렉터리 안의 CSV를 통째로 읽어 `{sheet: {word: reading}}` 형태로 반환하고, 규칙 함수들은 이 딕셔너리를 클로저로 감싸 `re.sub`에 넘길 치환 함수를 만든다. 새로운 약어 하나를 추가하는 일이 코드 변경이 아니라 CSV 한 줄 추가로 끝난다는 뜻이다.

---

# 발음의 핵심은 IPA다 — 한국어는 한 단계가 더 필요하다

정규화가 "무엇을 읽을지"를 결정한다면, phonemizer는 "그것을 어떻게 소리 낼지"를 결정한다. 여러 TTS 모델을 다뤄본 경험상, 텍스트를 문자 그대로 학습시키는 것보다 <abbr title="Grapheme-to-Phoneme, 문자를 발음 기호로 변환하는 과정" tabindex="0">G2P</abbr>를 거쳐 IPA로 학습시켰을 때 발음이 훨씬 자연스러웠다. 특히 영어처럼 철자와 발음의 괴리가 큰 언어에서 그 차이가 두드러졌다. 그래서 `tts-sentence-preprocessor`의 phonemizer 모듈은 최종적으로 IPA를 만들어내는 것을 목표로 하되, 언어별로 서로 다른 경로를 탄다.

![영어는 정규화 후 바로 IPA로 변환되는 2단계 파이프라인이고, 한국어는 정규화와 IPA 변환 사이에 경음화·비음화·유음화·구개음화 등 발음 규칙을 적용하는 G2P 단계가 추가된 3단계 파이프라인이다](/images/projects/tts-sentence-preprocessor-pipeline.svg)

영어는 정규화된 텍스트를 `phonemizer` 패키지의 `EspeakBackend`(espeak-ng 기반)에 그대로 넘기면 끝난다. `text_to_ipa("hello", language="en")`은 `"həlˈoʊ"`를 반환한다. espeak-ng이 영어의 발음 사전과 규칙을 이미 내장하고 있기 때문에, 정규화 다음 바로 IPA로 넘어가는 2단계로 충분하다.

한국어는 다르다. 자모를 IPA로 옮기는 매핑 자체는 위치에 따라 결정되는 단순한 테이블 조회다(`backend.py`의 `_ko_default()`). 문제는 이 테이블 조회가 표기된 자모를 "있는 그대로" IPA로 바꿀 뿐, 실제 발음에서 일어나는 경음화·비음화·유음화·구개음화 같은 음운 변화는 전혀 반영하지 않는다는 점이다. `core.py`의 `text_to_ipa()`에는 이 사실이 명시적으로 경고돼 있다 — 한국어 구간에 대해 음운 규칙을 적용하지 않고 raw jamo를 그대로 IPA로 매핑하므로, 발음학적으로 정확한 결과를 원한다면 `text_to_g2p()`를 먼저 호출해서 그 결과를 IPA 변환에 넘기라는 것이다. 실제로 "학교"를 G2P 없이 바로 IPA로 바꾸면 `hak̚gjo`가 나오지만, 이는 경음화가 반영되지 않은 잘못된 발음이다.

```python
>>> phonemizer.text_to_ipa("학교", language="ko")
'hak̚gjo'                 # G2P 생략 — 경음화 반영 안 됨

>>> g2p_text = phonemizer.text_to_g2p("학교")
>>> g2p_text
'학꾜'                     # 경음화(ㄱ+ㄱ → ㄱ+ㄲ) 적용
>>> phonemizer.text_to_ipa(g2p_text, language="ko")
'hak̚k͈jo'                # 실제 발음과 일치하는 IPA
```

즉 한국어는 **표기와 발음의 간극을 먼저 없앤 뒤에 IPA로 변환해야** 가장 자연스러운 결과가 나온다. 그 간극을 없애는 역할이 `korean_g2p.py`의 G2P 엔진이다. 음절을 초성·중성·종성 단위 자모로 분해한 뒤, 겹받침 단순화 → 구개음화 → 연음 → 격음화(aspiration) → 경음화(tensification) → 유음화(liquidization) 등 15단계의 규칙을 순서대로 적용하고, 마지막에 다시 음절 단위로 재조합한다. 규칙 하나하나가 이름이 붙은 별도 함수(`apply_gyeongeum`, `apply_yueum` 등)로 분리돼 있어서, 특정 규칙만 따로 테스트하거나 순서를 조정하기가 어렵지 않다.

---

# 규칙 기반이라 다 되는 건 아니다

이 접근의 장점은 동작이 투명하다는 것이다. 특정 단어의 발음이 이상하면 어느 규칙이 문제인지 역추적할 수 있고, 새로운 예외는 데이터나 규칙 함수 하나를 추가하는 문제로 좁혀진다. 다만 이는 곧 한계이기도 하다. 규칙과 사전 기반 접근은 언어를 새로 확장할 때마다 사람이 규칙 테이블을 직접 채워야 하고, `korean_g2p_constants.py`(600여 줄), `rules/korean.py`(500여 줄)처럼 규칙 테이블 자체가 상당한 분량을 차지한다.

몇 가지 기능은 아직 의도적으로 미완성 상태로 남겨뒀다. 영어 단어를 한국어 발음으로 옮기는 음역(예: "NASA" → "나사")은 로드맵에만 있고 구현되지 않았으며, 관련 테스트도 `skip` 처리돼 있다. 정확도가 검증되지 않은 기능을 슬쩍 넣어두는 대신, 안 되는 부분은 안 된다고 명시하는 쪽을 택했다. 개발 환경 면에서도 Windows에서는 한자 변환에 쓰는 `pyhanja`가 사전 빌드된 wheel을 제공하지 않아 MSVC Build Tools가 필요하고, `phonemizer`가 의존하는 espeak-ng도 DLL 경로를 직접 지정해줘야 하는 등 설치 마찰이 있다.

---

# 실제로 무엇이 달라졌는가

G2P 단계가 있고 없고의 차이는 테스트에 있는 최소 대응쌍들로 가장 분명하게 드러난다. 아래는 `tests/fixtures/phonemizer/korean_g2p_fixtures.py`에 있는 예시로, 표기 그대로는 틀리지만 G2P를 거치면 맞는 발음이 되는 경우들이다.

| 표기 | G2P 결과 | 적용된 규칙 |
| --- | --- | --- |
| 학교 | 학꾜 | 경음화: ㄱ+ㄱ → ㄱ+ㄲ |
| 국민 | 궁민 | 비음화: ㄱ+ㅁ → ㅇ+ㅁ |
| 신라 | 실라 | 유음화: ㄴ+ㄹ → ㄹ+ㄹ |
| 좋다 | 조타 | 격음화(aspiration): ㅎ+ㄷ → ㅌ |
| 없다 | 업따 | 겹받침 단순화 + 경음화 |
| 같이 | 가치 | 구개음화: ㅌ+이 → 치 |

여섯 개 모두 표기와 발음이 다르고, 그 차이가 규칙 하나로 설명 가능한 경우들이다. G2P 없이 이 표기들을 그대로 IPA로 바꾸면 자모 하나하나는 맞지만 문장 전체는 원어민이 듣기에 어색한 소리가 된다. 이 표는 동시에 회귀 테스트이기도 해서, 규칙을 추가하거나 순서를 바꿀 때마다 여섯 쌍이 여전히 맞는지 바로 확인할 수 있다.

---

# 사이드 프로젝트를 라이브러리로 만들며 배운 것

이 레포는 실제 서비스에서 쓰던 텍스트 전처리 로직의 핵심 컨셉을 가져와, 오픈소스로 공개할 수 있는 형태로 처음부터 다시 구성한 것이다. 실험 이름으로 분기 처리를 하드코딩하던 예전 방식 대신, 이번에는 그 분기를 `Pipeline`의 `postprocess_fn`/`custom_normalize_fn` 같은 훅으로 바꾸고, 정규화·phonemization 두 서브패키지를 완전히 독립적으로 설치할 수 있도록 `pyproject.toml`의 extras를 나눴다. 각각 pandas·pyhanja·unidecode·inflect(정규화)와 pandas·phonemizer(phonemization)만 있으면 되므로, 필요한 절반만 설치할 수 있게 됐다.

가장 크게 체감한 것은 <mark>텍스트 전처리가 TTS 품질에 기여하는 비중이 생각보다 훨씬 크다는 점</mark>이었다. 모델 구조나 파인튜닝 데이터에 시간을 쏟기 전에, 텍스트가 모델에 들어가기 전 어떤 형태로 바뀌는지부터 점검해볼 가치가 있다.

규칙 기반 언어 처리는 결코 우아하지 않다 — 수백 줄짜리 테이블과 정규식 매처가 늘어서 있는 코드는 논문에 실릴 만한 모습은 아니다. 하지만 적어도 왜 이렇게 읽히는지 설명할 수 있고, 예외 하나를 고치기 위해 전체를 다시 학습시킬 필요가 없다. <mark>이 두 가지 이유로, 프로덕션 환경에는 이쪽이 더 신뢰할 수 있는 선택이었다.</mark>
