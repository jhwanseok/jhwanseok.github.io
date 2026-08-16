---
layout: ../../layouts/ContentLayout.astro
title: "[스킬은 켜봐야 안다 #3] 말을 짧게 하면 정말 돈이 굳을까 — caveman을 큰 작업과 작은 작업에 나눠 시험하다"
date: 2026-08-12T12:00:00
tags: ["Engineering Experiments", "AI Engineering"]
description: "저자 스스로 '출력이 짧은 작업에서는 손해'라고 밝힌 caveman의 주장을 두 archetype에서 그대로 재현해본 기록"
---

저장소

- [GitHub: jhwanseok/skill-experiment-lab](https://github.com/jhwanseok/skill-experiment-lab)
- [실험 설계](https://github.com/jhwanseok/skill-experiment-lab/blob/main/experiments/design/caveman.md)
- [실행 결과](https://github.com/jhwanseok/skill-experiment-lab/blob/main/experiments/results/caveman.md)
- [정리된 리포트](https://github.com/jhwanseok/skill-experiment-lab/blob/main/experiments/results/caveman-report.md)

## 저자가 스스로 밝힌 한계를 그대로 재현해보기로 했다

[caveman](https://github.com/juliusbrussee/caveman)은 응답을 "이 소리 조각 다른 조각 비교, 카테고리 판단" 같은 간결한 문체로 압축하는 스킬이다. 앞선 두 실험과 달리 이번엔 화려한 벤치마크 숫자로 시작하지 않는다. caveman 저장소의 `HONEST-NUMBERS.md`는 첫 줄부터 "마케팅 없음. 당신의 작업에서 caveman이 손해라면, 이 페이지가 그렇게 말해줄 것"이라고 적어뒀다. 출력 토큰은 평균 65% 정도 준다고 밝히면서도, 입력 토큰(프롬프트·컨텍스트·파일)은 전혀 줄지 않고, SKILL.md를 매번 로드하는 고정 비용이 있어서 세션 전체로 보면 출력이 많은 작업에서만 14\~21% 순절감이고, 짧은 코딩 Q&A에서는 오히려 손해라고 저자 스스로 못 박아뒀다. 마케팅 문구가 아니라 저자 자신의 경고를 그대로 검증해볼 수 있는 드문 기회였다.

![caveman 도입 판단 요약 — 출력이 긴 작업에서는 세션 비용이 15.1% 줄었고, 출력이 짧은 작업에서는 오히려 9.9% 늘어 출력이 긴 작업에서만 조건부로 켜기로 판단했다](/images/projects/skill-experiment-caveman-verdict.svg)

결론부터 말하면 나는 이 스킬을 <mark>조건부로 쓴다.</mark> 저자가 예고한 대로 방향이 정확히 갈렸다. 출력이 긴 작업에서는 세션 비용이 15.1% 줄었고, 출력이 짧은 작업에서는 9.9% 늘었다. 새 픽스처를 만드는 대신 이미 검증된 두 상황을 그대로 재사용해 확인했다.

---

## 새 픽스처 없이, 이미 검증된 두 상황을 재사용했다

caveman은 특정 archetype에 묶여 있지 않으니, <mark>새 버그나 티켓을 또 만드는 대신 이미 확인된 두 상황을 그대로 재사용하기로 했다.</mark> 하나는 [ponytail 실험](/projects/skill-experiment-ponytail/)의 태그+필터링 티켓(출력이 긴 기능 추가 작업), 다른 하나는 [superpowers 실험](/projects/skill-experiment-superpowers/)의 대소문자 정렬 버그(출력이 짧은 디버깅 작업)다. `Agent(isolation: "worktree")` 경로에서 스킬이 아예 안 잡히는 것도 superpowers 실험과 같은 양상이라, 이번에도 처음부터 headless `claude -p` 세션으로 진행했다. 기능 추가 쪽은 metric 체계가 달라(이전엔 `subagent_tokens`, 이번엔 `cost_usd`) OFF/ON을 새로 6세션 돌렸고, 디버깅 쪽은 superpowers 실험의 OFF 데이터를 그대로 재사용하고 ON만 3세션 추가했다.

---

## 결과를 해석하다: 저자의 경고가 그대로 재현됐다

| Archetype | 지표 | OFF | ON | 차이 |
| --- | --- | --- | --- | --- |
| 1 (기능 추가, 긴 출력) | cost_usd | 0.8127 | 0.6896 | **−15.1%** |
| 1 | 응답 길이 | 932자 | 582자 | −37.6% |
| 2 (버그 수정, 짧은 출력) | cost_usd | 0.3416 | 0.3753 | **+9.9%** |
| 2 | 응답 길이 | 785자 | 376자 | −52.1% |

출력 자체는 두 상황 모두 확실히 짧아졌다(응답 길이 −37.6%, −52.1%). 문체를 압축한다는 caveman의 핵심 기능은 예외 없이 작동했다. <mark>그런데 그 압축이 세션 전체 비용으로 이어지는지는 정반대로 갈렸다.</mark> 원래 출력이 15,000토큰을 넘던 기능 추가 작업(archetype 1)에서는 압축분이 SKILL.md 로딩 비용을 훌쩍 넘어서 −15.1%의 순절감으로 남았고, 원래 출력이 3,500토큰 안팎이던 디버깅 작업(archetype 2)에서는 절대적인 압축량 자체가 작아서 로딩 비용을 감당하지 못하고 +9.9%로 뒤집혔다. 저자가 밝힌 breakeven 지점(출력 1,500\~2,000토큰 안팎)과 방향이 그대로 맞아떨어졌다.

품질 저하는 두 상황 모두에서 보이지 않았다. 기능 추가 쪽은 OFF/ON 6세션 모두 테스트가 통과했고(다만 ON 세션이 평균적으로 테스트를 더 적게 작성했다, 6.7개 vs 8.7개), 디버깅 쪽은 OFF/ON 6세션 모두 근본 원인(`COLLATE NOCASE`)을 정확히 고쳤다. caveman 자신이 "부정어·정확한 값은 절대 생략하지 않는다"고 정한 규칙도 12세션 전체에서 어긴 흔적이 없었다.

한계도 명시해둔다. n=3(archetype·조건별)이라 breakeven 지점은 방향만 확인했을 뿐 정밀 검증은 아니고, 두 archetype의 절대 비용은 작업 종류 자체가 달라 서로 비교할 수 없다. 응답 길이 지표는 채팅 최종 메시지만 잰 것이라 커밋 메시지·코드·도구 호출 서술은 포함하지 않는데, 이건 caveman 자신이 "채팅 밖에 남는 것(코드, 코멘트, 커밋)은 평소 문체로 쓴다"고 명시한 범위와 일치한다. archetype 2의 OFF 데이터는 superpowers 실험에서 재사용한 것이라 이 실험 시점에 활성화 여부를 별도로 진단하지는 않았다(다만 응답에서 caveman 특유의 문체는 육안으로도 확인되지 않았다).

---

## 이 실험이 바꾼 것

방향 자체는 저자의 경고와 정확히 일치했지만, 내 작업에 적용하려면 한 가지를 더 생각해야 했다. caveman은 "채팅 밖에 남는 것(코드, 코멘트, 커밋)은 압축하지 않는다"고 스스로 범위를 그어뒀다. 내가 주로 하는 작업 중 이 블로그 글쓰기는 결과물이 그대로 파일에 저장되는 산출물이라, 글 자체는 caveman이 건드리는 대상이 아니다. caveman이 실제로 줄이는 건 그 글을 쓰는 과정에서 오가는 대화형 설명·요약 같은 휘발성 응답이다. 그래서 <mark>이 작업(예: 이 시리즈처럼 여러 번 되짚으며 피드백을 주고받는 긴 세션)에서는 켜둘 만하고, 결과물이 파일 하나로 바로 끝나는 짧은 작업에서는 로딩 비용만 지는 셈이라 꺼둔다.</mark>

가장 흥미로웠던 건 실험 자체보다 검증 방식이었다. 이번엔 의심할 벤치마크가 없었다. 저자가 이미 정직하게 한계를 공개해뒀고, 내가 한 일은 그 공개된 한계가 실제로 재현되는지 확인하는 것뿐이었다. <mark>세 실험을 통틀어, 숫자를 의심하는 것 못지않게 "이 숫자가 성립하는 조건이 무엇인가"를 먼저 찾는 습관이 가장 오래 남을 것 같다.</mark>
