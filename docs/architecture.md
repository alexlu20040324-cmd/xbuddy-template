markdown
# StudentBuddy — System Architecture

## Graph Overview

START → initialize → router → generate_reply → generate_decision
                                    ↑                    ↓
                           └── memory_updater ───────────┘
                                     ↓
                             implementation → END


## Nodes

| Node | Role |
|---|---|
| `initialize` | 初始化对话状态，设定第一个 section = COURSE_INFO |
| `router` | 根据当前 section 和完成状态，决定下一步 |
| `generate_reply` | 调用 LLM，生成 AI 对用户的回复 |
| `generate_decision` | 判断当前 section 是否已收集到足够信息 |
| `memory_updater` | 把本轮对话存入 Supabase，更新 state |
| `implementation` | 生成最终 day-by-day study plan |

## State (XBuddyState)

| Field | Type | Description |
|---|---|---|
| `session_id` | str | 唯一对话 ID |
| `messages` | list | 完整对话历史 |
| `current_section` | SectionID | 当前进行的 section |
| `section_status` | SectionStatus | PENDING / COMPLETE |
| `collected_data` | dict | 各 section 收集到的用户信息 |
| `final_output` | str | 最终生成的 study plan |

## 5 Conversation Sections

| Section | ID | Purpose |
|---|---|---|
| 1 | `COURSE_INFO` | 收集大学、课程名称、课程代码 |
| 2 | `MATERIALS` | 列举可用学习材料 |
| 3 | `KNOWLEDGE_CHECK` | 自评掌握程度（1-10分） |
| 4 | `SCHEDULE` | 考试日期、每天可用学习时间 |
| 5 | `STUDY_PLAN` | 生成个性化 day-by-day 备考计划 |

## Tech Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph (StateGraph, conditional edges) |
| LLM interface | LangChain |
| Observability | LangSmith |
| API | FastAPI (streaming SSE + sync) |
| Database | Supabase |
| Frontend | Next.js + React |
