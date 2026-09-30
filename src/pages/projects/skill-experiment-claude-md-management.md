---
layout: ../../layouts/ContentLayout.astro
title: "[스킬은 켜봐야 안다 #5] CLAUDE.md에 몇 줄 적는 것만으로 얻는, claude-mem보다 싼 세션 간 기억"
date: 2026-09-30T18:00:00
tags: ["Engineering Experiments", "AI Engineering"]
description: "훅·워커·벡터DB 없이 CLAUDE.md 파일에 직접 쓰는 /revise-claude-md가 claude-mem보다 정확도와 비용 모두에서 앞선 유일한 사례를 검증한 기록"
---

저장소

- [GitHub: jhwanseok/skill-experiment-lab](https://github.com/jhwanseok/skill-experiment-lab)
- [실험 설계](https://github.com/jhwanseok/skill-experiment-lab/blob/main/experiments/design/claude-md-management.md)
- [실행 결과](https://github.com/jhwanseok/skill-experiment-lab/blob/main/experiments/results/claude-md-management.md)
- [정리된 리포트](https://github.com/jhwanseok/skill-experiment-lab/blob/main/experiments/results/claude-md-management-report.md)

## 훨씬 단순한데, 정말 더 쌀까

[claude-mem 실험](/projects/skill-experiment-claude-mem/)에서 확인한 것은 세 가지 대가였습니다. 활성화 자체의 실질 버그, 꾸준한 비용 증가, 그리고 자기검증 없는 staleness입니다. 그런데 정작 그 실험에서 가장 안정적으로 기록된 내용은 코드를 그렇게 구현한 이유 같은 일회성 맥락이 아니라, 이 환경에서 반복되는 툴링 함정이었습니다. 그렇다면 훨씬 가벼운 도구로 그 부분만 노려도 되지 않을까요.

`claude-md-management` 플러그인의 `/revise-claude-md` 커맨드는 세션이 끝날 때 배운 것을 CLAUDE.md, 곧 팀이 공유하는 파일에 몇 줄 적는 것이 전부입니다. 훅 체인도, 로컬 워커도, 벡터 DB도, 내부 요약 LLM 호출도 없습니다. CLAUDE.md는 어차피 매 세션이 시작될 때 자동으로 읽히는 파일이라, claude-mem이 필요로 했던 "검색" 단계 자체가 없습니다. 메커니즘이 이렇게 단순하면 claude-mem이 겪은 활성화 불안정성도 없으리라는 것이 이번 가설이었습니다.

![claude-md-management 실험 결론 요약: CLAUDE.md는 세션 시작 시 항상 로드되어 검색 단계가 없고, 정확도와 비용이 함께 개선된 유일한 사례로 확인돼 도입하기로 했다](/images/projects/skill-experiment-claude-md-management-verdict.svg)

미리 결론을 말하면, <mark>저는 이 스킬을 씁니다.</mark> 이 시리즈에서 정확도와 비용이 함께 개선된 것은 이번이 처음입니다. 환경 함정을 코드를 재실행하지 않고 정확히 경고하는 비율이 0/3에서 3/3으로 올랐는데, 같은 세션의 비용은 오히려 35.9% 줄었습니다. 다만 조건이 하나 붙습니다. 이 도구가 실제로 다루는 범위가 claude-mem보다 훨씬 좁습니다. 저는 세션1을 다 돌리고 나서야 그 사실을 알았습니다.

## 세션 1을 다 돌리고 나서야 질문을 바꿨다

세션1 티켓과 세션2 질문은 claude-mem 실험과 똑같은 문구를 재사용해서 비교 가능성을 맞췄습니다("북마크 태그 기능 추가" 다음에 "왜 그렇게 구현했는지, 코드는 다시 읽지 말고 답해줘"). 그런데 ON 조건 세션1을 3회 다 돌리고 CLAUDE.md 변경분을 확인해보니, 셋 다 태그 구현 내용은 전혀 적지 않았습니다. 대신 이 머신에서 `python -m venv .venv`가 `ensurepip` 오류로 실패한다는 로컬 환경 함정만 저장소 루트에 적어놨습니다.

플러그인 공식 문서를 다시 보니 이유가 있었습니다. "Reflect" 단계가 그 범위를 명시적으로 "bash commands, code patterns, testing approaches, environment quirks, gotchas"로 좁혀놨습니다. claude-mem처럼 "이번 세션에 있었던 일 전반"을 담는 범용 메모리가 아니라, 처음부터 "이 저장소에서 반복적으로 부딪힐 환경·툴링 함정"만 걸러 담도록 설계된 도구였습니다. 원래 질문을 그대로 쓰면 OFF와 ON 둘 다 "모른다"고 답할 뿐이라 무의미했습니다. 그래서 실제로 3/3 수렴해서 기록된 내용을 겨냥하도록 세션2 질문을 바꿨습니다. 실제로 물은 질문은 이렇습니다. "pytest를 돌려보려는데, 미리 알아두면 좋을 주의사항 있어?"

설치를 확인하는 과정에서 실수도 하나 있었습니다. `claude plugin install`을 무심코 실행했다가 이 머신의 전역 설정을 건드릴 뻔했습니다. 바로 `uninstall`로 되돌리고, 이후로는 claude-mem 실험처럼 `claude -p --settings`로 조건별 인라인 지정만 썼습니다. 이 과정에서 `--settings`가 전역 설정과 부분 병합된다는 것도 다시 확인했습니다. 전역으로 켜져 있던 `ponytail`과 `caveman`을 명시적으로 꺼주지 않으면 계속 섞여 들어왔습니다.

## 모르는 대가가 아는 것의 비용보다 컸다

| 지표 | OFF | ON | 차이 |
| --- | --- | --- | --- |
| 세션2 cost_usd | 0.3919 | 0.2514 | **−35.9%** |
| 세션2 num_turns | 14.3 | 8.7 | **−39.5%** |
| 세션1 cost_usd(오버헤드) | 0.8177 | 0.8150 | −0.3%(잡음) |
| venv 함정을 재실행 없이 경고 | 0/3 | 3/3 | 뚜렷한 차이 |

정확도를 끌어올리면서 비용까지 줄어든 이유는 OFF 조건이 치른 대가에 있었습니다. OFF-3은 venv 얘기를 아예 꺼내지 않았고, OFF-2는 "README대로 venv부터 만드세요"라며 이 머신에서 실패하는 것을 모른 채 틀린 조언을 했습니다. OFF-1은 그나마 근접했는데, 실제로 pytest를 재실행해서(21턴으로, 세 OFF 중 가장 비쌌습니다) "venv 없이도 되긴 하네" 정도를 우연히 확인했을 뿐 `ensurepip` 실패 자체는 몰랐습니다. 반면 ON 3세션은 전부 "CLAUDE.md에 적혀 있듯"이라고 출처를 직접 인용하며 8~10턴 만에 정확히 답했습니다. 모르는 대가, 곧 재탐색과 재실행이 아는 것의 비용, 곧 CLAUDE.md 몇 줄을 매번 읽는 것보다 컸습니다. claude-mem이 검색 파이프라인을 거치느라 캐시 미스 비용을 치른 것과는 정반대 구조입니다.

claude-mem과 나란히 놓아보면 차이가 선명합니다. claude-mem은 세션2 정확도를 얻는 대가로 세션2 비용을 30.3%, 세션1 비용도 21.1% 더 치렀습니다. `/revise-claude-md`는 정확도를 0/3에서 3/3으로 끌어올리면서 세션2는 오히려 35.9% 줄었고, 세션1 오버헤드는 잡음 수준인 −0.3%였습니다. 활성화도 더 안정적이었습니다. claude-mem이 3단계에 걸쳐 원인을 규명해야 했던 것과 달리, 파일럿에서 모델이 근거 없이 커맨드를 한 번 거부한 것 외에는 본 실행 3/3 전부 문제없이 기록됐습니다.

## 도입하되, claude-mem의 대체재로 읽지 않는다

<mark>이 결과를 claude-mem의 대체재로 읽으면 안 됩니다.</mark> 세 ON 세션 전부 태그 구현 방식은 기록하지 않고 환경 함정만 담았습니다. 이 도구는 애초에 "이번에 무엇을 왜 그렇게 만들었는지" 같은 일회성 맥락을 겨냥하지 않습니다. claude-mem이 노리던 범위와 이 도구가 실제로 잘하는 범위는 겹치지 않는, 서로 다른 문제입니다.

그래도 이 좁은 범위 안에서는 망설일 이유가 없었습니다. 메커니즘이 CLAUDE.md에 몇 줄 얹는 것이 전부라 검색 단계도, 활성화 불안정성도, staleness 위험도 없습니다. CLAUDE.md는 파일이라 코드와 함께 리뷰되고 버전 관리되니, claude-mem에서 가장 위험했던 문제, 곧 낡은 사실을 자기검증 없이 확신하는 것도 구조적으로 덜합니다.

다만 이번 실험은 단일 라운드였다는 한계가 있습니다. `/revise-claude-md`를 반복해서 쓰면 CLAUDE.md가 계속 불어나고, 그러면 이후 모든 세션이 매번 그 내용을 읽는 표준 비용이 늘어납니다. claude-mem에는 없는, 이 도구만의 트레이드오프입니다. 이 부분은 이번 실험 범위 밖이라 다음 숙제로 남겨둡니다.
