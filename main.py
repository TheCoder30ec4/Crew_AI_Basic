from dotenv import load_dotenv
from crewai import Crew
from tasks import MeetingPrepTasks
from agents import MeetingPrepAgents

def main():
    load_dotenv()
    print("## Welcome to the Meeting Prep Crew ##")
    meeting_participants = input("What are the names of the participants in the meeting?\n")
    meeting_context = input("What is the context of the meeting?\n")
    meeting_objective = input("What is your objective for this meeting?\n")

    tasks = MeetingPrepTasks()
    agents = MeetingPrepAgents()
    research_agent = agents.research_agent()
    industry_analysis_agent = agents.industry_analysis_agent()
    meeting_strategy_agent = agents.meeting_strategy_agent()
    summary_and_briefing_agent = agents.summary_and_briefing_agent()

    research_task = tasks.research_task(agent=research_agent, meeting_participants=meeting_participants,
                                        meeting_context=meeting_context)
    industry_analysis_task = tasks.industry_analysis_task(agent=industry_analysis_agent,
                                                          meeting_participants=meeting_participants,
                                                          meeting_context=meeting_context)
    meeting_strategy_task = tasks.meeting_strategy_task(agent=meeting_strategy_agent,
                                                        meeting_objective=meeting_objective,
                                                        meeting_context=meeting_context)
    summary_and_briefing_task = tasks.summary_and_briefing_task(agent=summary_and_briefing_agent,
                                                                meeting_context=meeting_context,
                                                                meeting_objective=meeting_objective)

    meeting_strategy_task.context = [research_task, industry_analysis_task]
    summary_and_briefing_task.context = [research_task, industry_analysis_task, meeting_strategy_task]

    crew = Crew(
        agents=[
            research_agent,
            industry_analysis_agent,
            meeting_strategy_agent,
            summary_and_briefing_agent
        ],
        tasks=[
            research_task,
            industry_analysis_task,
            meeting_strategy_task,
            summary_and_briefing_task
        ]
    )

    result = crew.kickoff()
    print(result)

if __name__ == "__main__":
    main()
