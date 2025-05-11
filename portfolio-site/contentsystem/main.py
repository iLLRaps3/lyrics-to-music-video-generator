import os
import nest_asyncio
from tinydb import TinyDB, Query
from typing import Dict, Optional, Generator, List
from textwrap import dedent
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableSerializable
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from gradio import Interface, Textbox, Markdown

# Apply nested asyncio for concurrent operations
nest_asyncio.apply()

# Initialize database
db = TinyDB("content_assistant_data.json")
content_table = db.table("viral_content")
hashtags_table = db.table("hashtags")

class ViralContentSystem:
    def __init__(self, api_key: str):
        """Initialize the viral content system with API key and database setup."""
        os.environ["GROQ_API_KEY"] = api_key
        self.memory = ConversationBufferMemory(memory_key="messages", return_messages=True)
        self.cycles = 3
        self.setup_agents()

    def create_agent(self, system_prompt: str, model_name: str, **llm_kwargs) -> RunnableSerializable[Dict, str]:
        """Create a Langchain LCEL chain agent with specified prompt and model."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages", optional=True),
            ("human", "{input}")
        ])

        llm = ChatGroq(model=model_name, **llm_kwargs)
        chain = prompt | llm | StrOutputParser()
        return chain

    def concat_response(self, inputs: Dict[str, str], reference_system_prompt: Optional[str] = None) -> str:
        """Concatenate and format responses from multiple agents."""
        default_prompt = dedent("""
        You have been provided with responses from various content creation agents.
        Synthesize these into a cohesive viral content strategy.
        Ensure all elements work together seamlessly for maximum viral potential.
        Agent responses:
        {responses}
        """)

        reference_system_prompt = reference_system_prompt or default_prompt
        responses = "\n".join(f"{i}. {out}" for i, out in enumerate(inputs.values()))
        return reference_system_prompt.format(responses=responses)

    def setup_agents(self):
        """Configure specialized agents for viral content creation."""
        self.agents = {
            'hook_creator_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are an expert at creating viral hooks for videos.
                Identify the most shocking/interesting moment from the script and craft a compelling 
                5-10 second hook that will stop users from scrolling. Focus on creating curiosity gaps
                and emotional triggers. {helper_response}""",
                model_name='llama3-8b-8192'
            ),
            
            'shorts_script_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are a master at writing viral short-form video scripts (30-60 seconds).
                Create engaging, fast-paced scripts that maintain viewer attention throughout.
                Include pattern interrupts, emotional triggers, and clear call-to-actions.
                Format output as a proper script with timestamps and visual directions. {helper_response}""",
                model_name='llama3-8b-8192'
            ),
            
            'long_script_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are an expert at writing 3-5 minute viral video scripts.
                Create compelling narratives that maintain engagement while providing value.
                Include storytelling elements, emotional peaks and valleys, and strategic pattern interrupts.
                Format output as a proper script with timestamps, visual directions, and B-roll suggestions. {helper_response}""",
                model_name='llama3-groq-70b-8192-tool-use-preview'
            ),
            
            'title_optimization_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are a specialist in creating viral titles for different platforms.
                Create platform-specific titles that maximize CTR while following best practices:
                - TikTok: Short, emotionally charged, with 3 relevant hashtags
                - YouTube: SEO-optimized, curiosity-driving, with 3 strategic hashtags
                - Instagram: Engaging, relatable, with 3 trending hashtags
                Provide 3 variations for each platform. {helper_response}""",
                model_name='llama3-8b-8192'
            ),
            
            'description_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are an expert at crafting viral video descriptions.
                Create platform-optimized descriptions that:
                - Drive engagement and encourage comments
                - Include strategic hashtags (200+ for TikTok, 25 for YouTube)
                - Incorporate relevant keywords for searchability
                - Include timestamps for longer videos
                - Add calls-to-action and hooks {helper_response}""",
                model_name='llama3-8b-8192'
            ),
            
            'hashtag_strategy_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are a hashtag optimization specialist.
                Create platform-specific hashtag strategies:
                - TikTok: 200+ trending and niche hashtags
                - YouTube: 25 strategic hashtags for searchability
                - Instagram: Mix of trending and targeted hashtags
                Research current trends and provide hashtag groupings by:
                - Trending tags
                - Niche-specific tags
                - Engagement-driving tags {helper_response}""",
                model_name='llama3-8b-8192'
            ),
            
            'viral_techniques_agent': RunnablePassthrough() | self.create_agent(
                system_prompt="""You are an expert in viral content techniques.
                Analyze the script and suggest implementing:
                - Pattern interrupts (visual/audio)
                - Psychological triggers
                - Storytelling elements
                - Engagement hooks
                - Retention strategies
                Provide specific timestamps for implementing each technique. {helper_response}""",
                model_name='llama3-groq-70b-8192-tool-use-preview'
            )
        } | RunnableLambda(self.concat_response)

        self.main_agent = self.create_agent(
            system_prompt="""You are an advanced viral content strategist.
            Combine all agent responses into a comprehensive content strategy.
            Ensure the hook, script, titles, descriptions, and hashtags work together
            cohesively for maximum viral potential. Provide a final content brief
            that includes all elements organized by platform. {helper_response}""",
            model_name="llama3-groq-70b-8192-tool-use-preview",
            temperature=0.7,
        )

    def process_content_request(self, topic: str) -> Generator[str, None, None]:
        """Process content creation request through the agent pipeline."""
        llm_input = {
            'input': topic,
            'messages': self.memory.load_memory_variables({}).get('messages', []),
            'helper_response': ""
        }

        for _ in range(self.cycles):
            responses = self.agents.invoke(llm_input)
            llm_input['helper_response'] = responses

        final_response = self.main_agent.invoke(llm_input)
        yield final_response

def create_interface(content_system):
    """Create and configure the Gradio interface."""
    def handle_input(topic: str):
        output = ""
        for response in content_system.process_content_request(topic):
            output += response + "\n"
            yield output

    interface = Interface(
        fn=handle_input,
        inputs=[Textbox(label="Enter Your Video Topic or Concept", lines=5, 
                       placeholder="Describe your video idea or topic...")],
        outputs=[Markdown(label="Viral Content Strategy")],
        live=True,
        title="Viral Content Creation Assistant"
    )
    return interface

if __name__ == "__main__":
    # Initialize the content system with your API key
    content_system = ViralContentSystem(api_key="your-groq-api-key")
    
    # Create and launch the interface
    interface = create_interface(content_system)
    interface.launch(debug=True)
