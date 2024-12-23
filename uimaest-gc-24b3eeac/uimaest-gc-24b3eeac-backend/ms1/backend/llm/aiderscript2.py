from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import os

class ReactComponentCoder2:
    """
    A class to facilitate the development and error resolution of React components using AI models.

    This class provides methods to initialize a coding environment, generate UI components, and resolve
    errors in React applications. It leverages AI models to assist in these tasks.
    """

    def __init__(self, model_name="gpt-4o", weak_model_name="gpt-4-turbo"):
        """
        Initializes the ReactComponentCoder with specified AI models.

        Args:
            model_name (str): The name of the main AI model to use.
            weak_model_name (str): The name of the weaker AI model to use for certain tasks.
        """

        self.io = InputOutput(yes=True)
        self.model = Model(model_name, weak_model=weak_model_name)
        self.coder = None

    def extract_file_paths(self, src):
        """
        Extracts file paths of JSX components from a specified source directory.

        Args:
            src (str): The source directory to search for JSX files.

        Returns:
            list: A list of file paths for JSX components found in the directory.
        """
        
        # Define the images directory
        images_dir = os.path.abspath(os.path.join(src, "../../../images"))
        json_dir=os.path.abspath(os.path.join(src,"../../../../backend/output.txt"))
        custom_css=os.path.abspath(os.path.join(src,"../../../../backend/industrial-ui-docs.txt"))


        src = f"{src}/src/Components"
        
        file_paths = []
        for root, dirs, files in os.walk(src):
            for file in files:
                if file.split(".")[-1] == "jsx":
                    file_paths.append((root + "/" + file).replace("../", "").replace("\\", "/"))

        print(custom_css)
        if os.path.isfile(custom_css):
        # If it's a file and has a .txt extension, append its path to file_paths
            if custom_css.endswith(".txt"):
                file_paths.append(custom_css.replace("../", "").replace("\\", "/"))
                
        print(file_paths)
        return file_paths

    def init_aider(self, dir):
        """
        Initializes the coding environment with the specified directory.

        Args:
            dir (str): The directory containing the React application.

        This method extracts file paths of JSX components and initializes the Coder with these files.
        """

        fnames = self.extract_file_paths(dir)
        fnames.append(f"{dir}/src/App.jsx")
        print(fnames)

        self.coder = Coder.create(main_model=self.model, io=self.io, fnames=fnames)

    def generate_ui(self, inp, dir,docs,user_prompt):
        
        calculator="""
        import React, { useState } from 'react';
        import { Button,Input } from '@actyx/industrial-ui';

        const TodoApp = () => {
        const [input, setInput] = useState('');
        const [result, setResult] = useState('');

        const handleClick = (value) => {
        setInput((prev) => prev + value);
        };

        const calculateResult = () => {
        try {
        // Use a safer alternative to eval here if possible
        setResult(eval(input)); // Note: eval is used for simplicity, consider a safer alternative
        } catch (error) {
        setResult('Error');
        }
        };

        const clearInput = () => {
        setInput('');
        setResult('');
        };

        return (
        <div>
        <Input type="text" value={input} readOnly />
        <Input type="text" value={result} readOnly />
        <div>
        <Button color='primary' text="1" variant='raised' onClick={() => handleClick('1')}></Button>
        <Button color='primary' text="2" variant='raised' onClick={() => handleClick('2')}></Button>
        <Button color='primary' text="3" variant='raised' onClick={() => handleClick('3')}></Button>
        <Button color='primary' text="+" variant='raised' onClick={() => handleClick('+')}></Button>
        </div>
        <div>
        <Button color='primary' text="4" variant='raised' onClick={() => handleClick('4')}></Button>
        <Button color='primary' text="5" variant='raised' onClick={() => handleClick('5')}></Button>
        <Button color='primary' text="6" variant='raised' onClick={() => handleClick('6')}></Button>
        <Button color='primary' text="-" variant='raised' onClick={() => handleClick('-')}></Button>
        </div>
        <div>
        <Button color='primary' text="7" variant='raised' onClick={() => handleClick('7')}></Button>
        <Button color='primary' text="8" variant='raised' onClick={() => handleClick('8')}></Button>
        <Button color='primary' text="9" variant='raised' onClick={() => handleClick('9')}></Button>
        <Button color='primary' text="*" variant='raised' onClick={() => handleClick('*')}></Button>
        </div>
        <div>
        <Button color='primary' text="C" variant='raised' onClick={clearInput}></Button>
        <Button color='primary' text="0" variant='raised' onClick={() => handleClick('0')}></Button>
        <Button color='primary' text="=" variant='raised' onClick={calculateResult}></Button>
        <Button color='primary' text="/"variant='raised' onClick={() => handleClick('/')}></Button>
        </div>
        </div>
        );
        };

        export default TodoApp;
        """
        
        
        
        ToDo="""
                import React, { useState } from 'react';
        import { Button, Input } from '@actyx/industrial-ui'; // Assuming these are the correct imports from the documentation

        const TodoApp = () => {
            const [tasks, setTasks] = useState([]);
            const [task, setTask] = useState('');
            const [filter, setFilter] = useState('');

            const addTask = () => {
                if (task) {
                    setTasks([...tasks, { text: task, completed: false }]);
                    setTask('');
                }
            };

            const deleteTask = (index) => {
                const newTasks = tasks.filter((_, i) => i !== index);
                setTasks(newTasks);
            };

            const toggleTaskCompletion = (index) => {
                const newTasks = tasks.map((task, i) =>
                    i === index ? { ...task, completed: !task.completed } : task
                );
                setTasks(newTasks);
            };

            const filteredTasks = tasks.filter(task =>
                task.text.toLowerCase().includes(filter.toLowerCase())
            );

            return (
                <div style={{ padding: '20px' }}>
                    <h1>To-do App</h1>
                    <Input
                        value={task}
                        onChange={(e) => setTask(e.target.value)}
                        placeholder="Add a new task"
                    />
                    <Button color='primary' text="Add Task" variant='raised' onClick={addTask}></Button>
                    <Input
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                        placeholder="Search tasks"
                    />
                    <ul>
                        {filteredTasks.map((task, index) => (
                            <li key={index} style={{ textDecoration: task.completed ? 'line-through' : 'none' }}>
                                {task.text}
                                <Button color='primary' text="Completed" variant='raised' onClick={() => toggleTaskCompletion(index)}>
                                    {task.completed ? 'Undo' : 'Complete'}
                                </Button>
                                <Button color='primary' text="Delete" variant='raised' onClick={() => deleteTask(index)}></Button>
                            </li>
                        ))}
                    </ul>
                </div>
            );
        };

        export default TodoApp;
        """
        
        QuizApp="""
                import React, { useState } from 'react';
        import { Button, Input } from '@actyx/industrial-ui'; // Assuming these are the correct imports from the provided CSS library

        const QuizApp = () => {
            const [currentQuestion, setCurrentQuestion] = useState(0);
            const [score, setScore] = useState(0);
            const [userAnswers, setUserAnswers] = useState([]);
            const questions = [
            {
                question: "What is the capital of France?",
                options: ["Berlin", "Madrid", "Paris", "Lisbon"],
                answer: "Paris"
            },
            {
                question: "What is 2 + 2?",
                options: ["3", "4", "5", "6"],
                answer: "4"
            },
            {
                question: "What is the largest planet in our solar system?",
                options: ["Earth", "Mars", "Jupiter", "Saturn"],
                answer: "Jupiter"
            },
            {
                question: "What is the boiling point of water?",
                options: ["90°C", "100°C", "110°C", "120°C"],
                answer: "100°C"
            },
            {
                question: "Who wrote 'To Kill a Mockingbird'?",
                options: ["Harper Lee", "J.K. Rowling", "Ernest Hemingway", "Mark Twain"],
                answer: "Harper Lee"
            },
            {
                question: "What is the chemical symbol for gold?",
                options: ["Au", "Ag", "Pb", "Fe"],
                answer: "Au"
            },
            {
                question: "Who painted the Mona Lisa?",
                options: ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"],
                answer: "Leonardo da Vinci"
            },
            {
                question: "What is the capital of Japan?",
                options: ["Seoul", "Beijing", "Tokyo", "Bangkok"],
                answer: "Tokyo"
            },
            {
                question: "What is the smallest prime number?",
                options: ["0", "1", "2", "3"],
                answer: "2"
            },
            {
                question: "Who is known as the father of computers?",
                options: ["Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs"],
                answer: "Charles Babbage"
            },
            {
                question: "What is the speed of light?",
                options: ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"],
                answer: "300,000 km/s"
            },
            {
                question: "What is the largest ocean on Earth?",
                options: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                answer: "Pacific Ocean"
            }
            ];

            const handleAnswer = (option) => {
                setUserAnswers([...userAnswers, option]);
                if (option === questions[currentQuestion].answer) {
                    setScore(score + 1);
                }
                if (currentQuestion < questions.length - 1) {
                    setCurrentQuestion(currentQuestion + 1);
                } else {
                    alert(`Quiz finished! Your score is ${score + 1}/${questions.length}`);
                }
            };

            return (
                <div style={{ padding: '20px', textAlign: 'center' }}>
                    <h1>Quiz App</h1>
                    <div>
                        <h2>{questions[currentQuestion].question}</h2>
                        {questions[currentQuestion].options.map((option, index) => (
                            <Button color='primary' text= {option} variant='raised' key={index} onClick={() => handleAnswer(option)} style={{ margin: '5px' }}>

                            </Button>
                        ))}
                    </div>
                </div>
            );
        };

        export default QuizApp;
        """
        
        
        YoutubePage="""
                import React from 'react';
        import { Button, Typography, Input } from '@actyx/industrial-ui';
        
        const YouTubeFrontPage = () => {
        return (
            <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <Typography variant="h1" bold={true}>YouTube</Typography>
                <div style={{ display: 'flex', alignItems: 'center', flex: 1, margin: '0 20px' }}>
                <Input type="text" placeholder="Search" style={{ flex: 1, marginRight: '10px' }} />
                <Button color="primary" text="Search" />
                </div>
                <div>
                <Button color="secondary" text="Sign In" style={{ marginRight: '10px' }} />
                <Button color="secondary" text="Sign Up" />
                </div>
            </header>
            <main>
                <section style={{ marginBottom: '40px' }}>
                <Typography variant="h2" bold={true}>Trending Videos</Typography>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
                    {/* Add video components here */}
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                </div>
                </section>
                <section>
                <Typography variant="h2" bold={true}>Recommended for You</Typography>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
                    {/* Add video components here */}
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                    <div style={{ width: '300px', height: '200px', backgroundColor: '#ccc' }}></div>
                </div>
                </section>
            </main>
            <footer style={{ marginTop: '40px', textAlign: 'center' }}>
                <Typography variant="body1">© 2023 YouTube</Typography>
            </footer>
            </div>
        );
        };
        
        export default YouTubeFrontPage;
        """
        
        
        
        """
        Generates or updates UI components based on the provided input.

        Args:
            inp (str): The input or instructions for generating UI components.
            dir (str): The directory where the React application is located.

        This method uses AI to generate or update React components, ensuring proper styling and imports.
        """

        dir = dir.replace("\\", "/")
        system1 = f"""
            "If you are creating todo app take the code from {ToDo}.
            If you are creating Calculator take the code from {calculator}.
            If you are creating Youtube front page take the code from {YoutubePage}.
            If you are creating quiz app take the code from {QuizApp}.
            Otherwise use CSS Library Documentation:\n{docs}\n\n use this for styling and do not add any extra css files.
            Use the components properly as mentioned in the file with very accurate props mentioned (take reference from) 
            examples of the components in the documentation. also if you require any extra css use inline css
            Don't use default css and components. Use components only from the document which i have provided.
            Only use the css from css library documenation and use proper imports and use their variants and User Prompt:\n{user_prompt}
            Do no generate hypothetical components and styles ,
            only use styles and components from given library and use proper imports
            Generate the corresponding React code:
            Also import that component in App.jsx.
            Always create new components inside {dir}/src/Components folder.
        """
        query = inp
        input = system1 + query
        self.coder.run(input)

    def resolve_error(self, inp):
        """
        Resolves errors in React code based on the provided error input.

        Args:
            inp (str): The error message or description to be resolved.

        This method uses AI to analyze and resolve errors in React applications.
        """

        system1 = f"""
            You are a smart React js developer who can understand and resolve errors in React js code
            your task is to analyze the error {inp} and perform necessary actions to resolve the error.
        """
        query = inp
        input = system1 + query
        self.coder.run(input)
    
    def clear_history_files(self):
        """ Clear the history files"""
        
        self.coder.run("/reset")