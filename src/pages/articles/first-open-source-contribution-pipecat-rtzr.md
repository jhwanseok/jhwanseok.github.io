---
layout: ../../layouts/ContentLayout.astro
title: "첫 오픈소스 기여: 이슈를 기다리는 대신 한국어 STT 플러그인을 만들다"
date: 2026-10-22T20:00:00
tags: ["Voice AI", "Engineering Notes"]
description: "good first issue를 찾다가 방향을 바꿔, 음성 에이전트 프레임워크 Pipecat에 RTZR 한국어 스트리밍 STT를 붙이는 패키지와 문서 PR을 만들기까지 저장소를 고른 기준과 리뷰에서 배운 점을 정리합니다."
---

관련 링크

- [GitHub: jhwanseok/pipecat-rtzr](https://github.com/jhwanseok/pipecat-rtzr)
- [PyPI: pipecat-rtzr](https://pypi.org/project/pipecat-rtzr/)
- [pipecat-ai/docs PR #1573: RTZR 서비스 문서](https://github.com/pipecat-ai/docs/pull/1573)
- [Pipecat Community Integrations Guide](https://github.com/pipecat-ai/pipecat/blob/main/COMMUNITY_INTEGRATIONS.md)

## 말로 설명하던 것을 코드로 남기고 싶었습니다

저는 일터에서 음성 AI와 콜센터(<abbr title="AI Contact Center: AI가 상담 업무를 함께 처리하는 콜센터 시스템" tabindex="0">AICC</abbr>) 시스템을 만듭니다. 전화 음성은 8kHz로 좁게 들어오고, 고객은 상담 도중에 말을 끊습니다. 말이 끝났는지 판단이 늦어지면 봇의 대답도 그만큼 늦어집니다. 이런 감각은 일하면서 조금씩 쌓이지만, 밖에서 보면 이력서의 한 줄이나 글 속의 설명으로만 남습니다. 설명은 읽는 사람이 믿어 줘야 성립합니다.

그래서 누구나 읽고, 설치하고, 직접 돌려 볼 수 있는 공개 코드로 남겨 보기로 했습니다. 그 방법으로 고른 것이 오픈소스 기여였습니다. 시작하면서 정한 원칙도 하나 있었습니다. 저는 코드를 쓸 때 Claude를 함께 쓰는데, 이 사실을 숨기지 않고 PR에 그대로 밝히기로 했습니다.

처음 계획은 이슈 하나를 골라 고치는 것이었지만, 그 계획대로 되지는 않았습니다. 결국 음성 에이전트 프레임워크 Pipecat에 한국어 스트리밍 STT를 붙이는 패키지 `pipecat-rtzr`를 만들어 PyPI에 0.1.0으로 올렸고, Pipecat 공식 문서에 이 패키지를 등록하는 PR을 보냈습니다. 문서 PR은 첫 리뷰에서 지적 두 개만 고치면 머지하겠다는 답을 받았고, 두 가지를 고친 뒤 머지되었습니다. 그런데 그 두 개는 코드가 아니라 그 프로젝트의 관례에 관한 것이었습니다.

## 이슈 대신 아직 없는 통합을 만들기로 했습니다

처음에는 sherpa-onnx, silero-vad, livekit/agents 같은 음성 에이전트 저장소에서 "good first issue"를 찾아봤습니다. 그런데 열어 본 이슈들은 이미 구현되어 있거나 다른 기여자가 처리한 상태였습니다. 그래서 이슈가 나오기를 기다리는 대신, 제가 잘 아는 한국어 음성 쪽에서 아직 없는 통합을 직접 만들기로 했습니다.

어디에 붙일지는 기여 방식을 보고 정했습니다. LiveKit에는 RTZR 플러그인이 이미 있었고, 새 플러그인 PR은 리뷰를 받기까지 오래 걸리고 있었습니다. Pipecat은 커뮤니티 통합을 본 저장소에 넣지 않습니다. 기여자가 자기 저장소에 패키지를 만들어 배포하고 유지하며, Pipecat 문서 저장소에는 그 패키지를 소개하는 PR과 30~60초 정도의 데모 영상만 보냅니다. 가이드에 따르면 Pipecat 팀은 커뮤니티 통합의 코드를 리뷰하거나 테스트하지 않으므로, 코드의 품질은 기여자가 책임져야 합니다. PyPI에는 아직 `pipecat-rtzr`라는 패키지가 없었습니다.

붙일 STT로는 리턴제로(RTZR)의 VITO를 골랐습니다. WebSocket 스트리밍 API를 제공하고, `sommers_ko` 모델이 한국어 8kHz 전화 음성에 맞춰져 있어서 콜센터 음성 에이전트에 잘 맞습니다.

## Pipecat에서 STT는 바꿔 끼울 수 있는 한 칸입니다

Pipecat의 파이프라인은 프로세서를 한 줄로 이어 놓은 구조이고, 프로세서 사이로 프레임이 흐릅니다. 오디오 입력 프로세서는 마이크 오디오를 오디오 프레임으로 내보내고, 함께 붙은 <abbr title="Voice Activity Detection: 소리 중에서 사람이 말하는 구간을 찾아내는 기능" tabindex="0">VAD</abbr>는 사용자가 말을 멈췄다는 프레임을 보냅니다. STT 서비스는 오디오 프레임을 받아 텍스트 프레임을 내보내고, 그 뒤의 LLM과 TTS는 앞에 어떤 STT가 있는지 알지 못합니다. 그래서 STT 한 칸만 RTZR로 바꾸면 나머지 파이프라인은 그대로 둔 채 한국어 음성을 받을 수 있습니다.

![Pipecat 파이프라인 속 RTZRSTTService의 자리를 보여주는 다이어그램. 파이프라인은 오디오 입력(VAD 포함), RTZR STT, 사용자 문맥, LLM, TTS, 오디오 출력을 한 줄로 잇는다. RTZR STT는 아래의 RTZR VITO 스트리밍 API와 WebSocket으로 연결되어 PCM 오디오를 보내고 interim과 final 결과를 받는다. 오른쪽 카드는 서비스가 소켓 위에서 지키는 약속을 정리한다. VAD가 발화 끝을 알리면 Finalize로 바로 닫고, 종료할 때 EOS를 보낸 뒤 마지막 final을 최대 2초 기다리고, 무음 60초면 서버가 끊으므로 무음을 보내 연결을 유지하고, 토큰은 캐시했다가 401이면 한 번 재시도하고, 키워드 부스팅을 지원한다. 아래 주의 상자는 끊기면 자동으로 다시 연결하지만 진행 중이던 발화는 사라진다고 적는다.](/images/articles/pipecat-rtzr-stt-pipeline.svg)

사용하는 쪽에서 보면 파이프라인에 서비스 하나를 넣는 것으로 끝납니다.

```python
from pipecat_rtzr import RTZRSTTService

stt = RTZRSTTService(
    settings=RTZRSTTService.Settings(
        domain="CALL",
        use_punctuation=True,
        keywords=[("리턴제로", 3.0), "상담원"],
    ),
)

pipeline = Pipeline([transport.input(), stt, user_aggregator, llm, tts, transport.output()])
```

`RTZRSTTService`는 Pipecat의 `WebsocketSTTService`를 상속합니다. 소켓을 열고 오디오를 흘려보내는 큰 틀은 Pipecat이 제공하고, 제가 채운 것은 RTZR 서버와의 약속을 지키는 부분입니다. 말하는 도중의 중간 결과(interim)는 중간 프레임으로, 확정된 결과(final)는 확정 프레임으로 바꿔 내보냅니다.

가장 신경 쓴 부분은 발화의 끝입니다. RTZR 서버도 스스로 발화 끝을 판단하지만, Pipecat 쪽 VAD가 먼저 사용자가 말을 멈췄다고 알리면 `Finalize` 메시지를 보내 그 발화를 바로 닫습니다. 데모 영상에서는 VAD가 발화 끝을 알린 뒤 약 30ms 만에 마지막 발화가 닫힙니다. 콜센터 봇에서는 STT가 발화를 닫아야 LLM이 답을 만들기 시작하므로, 이 구간이 짧을수록 응답이 빨라집니다.

연결의 처음과 끝도 챙겨야 했습니다. 접속 토큰은 캐시해 두었다가 만료되기 전에 새로 받고, 접속이 HTTP 401로 거절되면 토큰을 다시 받아 한 번 더 시도합니다. RTZR은 오디오가 60초 동안 들어오지 않으면 소켓을 닫기 때문에, 사용자가 말하지 않는 동안에는 무음 오디오를 보내 연결을 유지합니다. 파이프라인이 끝날 때는 `EOS`를 보내 서버가 마지막 발화를 정리하게 하고, 그 결과를 최대 2초(기본값) 기다립니다. 상담원 이름이나 상품명처럼 자주 틀리는 단어에는 키워드 부스팅으로 가중치를 줄 수 있습니다.

하지 못하는 것도 README에 그대로 적었습니다. 소켓이 끊기면 서비스가 자동으로 다시 연결하지만, 끊긴 순간 말하고 있던 발화의 오디오는 다시 보내지 않으므로 그 발화는 사라집니다. 그리고 지금까지는 합성한 짧은 한국어 음성으로만 확인했고, 실제 전화 음성과 긴 통화로는 아직 시험하지 않았습니다. README에는 0.1.0을 알파로 표시하고 이 두 가지를 함께 적어 두었습니다.

테스트는 두 층으로 나눴습니다. 단위 테스트와 RTZR 서버를 흉내 낸 mock 서버 테스트는 자격 증명 없이 돌아가므로 누구나 저장소를 받아 바로 실행할 수 있습니다. 그 위에서 2026년 10월 21일에 실제 RTZR API로 스트리밍, `Finalize`, `EOS`, 토큰 갱신, 재연결을 확인했습니다. 실제 API로 스트리밍하는 32초 데모 영상은 v0.1.0 릴리스에 올려 두었습니다.

## 리뷰에서 지적받은 것은 코드가 아니라 관례였습니다

문서 PR([pipecat-ai/docs#1573](https://github.com/pipecat-ai/docs/pull/1573))은 네 가지로 구성했습니다. RTZR 서비스 페이지를 새로 만들고, Supported Services 표에 한 줄을 넣고, 내비게이션에 항목을 추가하고, 문서 전체를 LLM이 읽기 좋게 모아 둔 llms.txt를 다시 생성했습니다.

첫 리뷰는 메인테이너 markbackman에게서 왔습니다.

> Two nits and then this is ready to be merged

지적은 두 가지였습니다. 첫째, 설치 안내는 관례대로 `uv` 명령만 보여 달라는 것이었습니다. 저는 `uv add`와 `pip install`을 함께 적었는데, 이 문서는 설치 방법을 하나로 통일하고 있었습니다. 둘째, 새로 만드는 페이지에는 redirect를 넣지 않는다는 것이었습니다. 저는 가이드에 적힌 대로 redirect 항목을 추가했습니다. 그런데 기존 redirect 항목들은 예전 주소(`/server/services/...`)를 지금 주소(`/api-reference/server/services/...`)로 넘겨 주는 용도였습니다. 처음 생기는 페이지에는 넘겨 줄 예전 주소가 없습니다. 돌아보면 당연한 이야기인데, 가이드 문장을 그대로 따르다 보니 그 항목이 왜 있는지는 확인하지 못했습니다.

두 가지 모두 PR을 올린 날 밤에 고쳐서 올렸습니다. 그리고 두 시간쯤 뒤인 10월 23일 새벽(한국 시간), markbackman이 PR을 머지했습니다. 이제 Pipecat 문서 저장소의 Supported Services 표에는 RTZR이 커뮤니티 통합으로 한 줄 들어가 있습니다.

PR 설명에는 처음 정한 원칙대로 AI를 어떻게 썼는지 적었습니다.

> With help from Claude, I wrote this integration and its documentation. I reviewed the code and the docs, and I ran the tests and the live checks.

Claude의 도움으로 통합 코드와 문서를 썼고, 코드와 문서는 제가 검토했으며, 테스트와 실제 API 확인도 제가 직접 돌렸다는 내용입니다. 무엇을 맡기고 무엇을 직접 했는지를 나눠서 밝히는 편이 읽는 사람에게도, 저에게도 분명하다고 생각했습니다.

이번 기여에서 배운 것은 세 가지입니다.

첫째, 코드보다 기여 경로를 먼저 읽어야 합니다. 저는 코드를 쓰기 전에 이슈의 실제 상태, 닫힌 PR의 이력, 기여 가이드를 읽는 데 먼저 시간을 썼고, 그 결과가 어디에 무엇을 기여할지를 정했습니다. 같은 RTZR 통합이라도 LiveKit에 냈다면 이미 있는 플러그인과 겹쳤을 것입니다.

둘째, 작은 관례가 리뷰를 좌우합니다. 두 지적 모두 기능과는 상관이 없었지만, 그것을 고치기 전까지는 머지되지 않습니다. <mark>가이드에 적힌 절차도 그 절차가 왜 있는지까지 이해해야 상황에 맞게 적용할 수 있었습니다.</mark>

셋째, mock이 아니라 실제 API로 확인해야 합니다. mock 서버는 제가 이해한 RTZR의 동작을 흉내 낼 뿐입니다. mock 테스트가 모두 통과해도, 그것이 보여 주는 것은 코드가 제 이해대로 움직인다는 사실까지입니다. 그 이해가 맞는지는 실제 서버에 `Finalize`와 `EOS`를 보내 봐야 알 수 있었습니다.

## 다음 기여도 제가 잘 아는 문제가 있는 곳에서 하려고 합니다

다음 기여처는 음성 에이전트, LLM, 그리고 에이전트와 SDK의 세 갈래로 살펴보고 있습니다. 후보를 고르는 기준은 이번 경험에서 그대로 가져왔습니다. 메인테이너가 외부 PR에 얼마나 빨리 응답하는지, 외부 기여자의 PR이 실제로 얼마나 머지되는지, AI 사용에 관한 정책이 무엇인지, 그리고 한국어 음성과 콜센터라는 제 배경이 그 프로젝트에서 쓸모가 있는지입니다.

모든 기여를 글로 남기지는 않을 생각입니다. 다음 글은 이 기준으로 고른 저장소에서 의미 있는 기여를 했을 때 쓰겠습니다.
