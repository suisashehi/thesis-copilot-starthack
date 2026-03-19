import type { Match } from '../types/thesis'

export const MOCK_MATCHES: Match[] = [
  {
    id: '1',
    title: 'AI-Driven Energy Optimization System',
    company: 'GreenTech AG',
    companyInitial: 'G',
    score: 98,
    tags: ['Python', 'Machine Learning', 'Energy'],
    matchReason: 'Matches your Python skills + Energy intent',
    summary:
      'Develop an ML pipeline that forecasts energy consumption patterns across Swiss smart grids. The system will integrate real-time sensor data, apply time-series models, and output optimization signals to reduce peak-load waste by up to 30%. Run in collaboration with ETH Zurich and funded until 2027.',
    contact: 'Dr. Mia Keller · m.keller@greentech.ch',
  },
  {
    id: '2',
    title: 'Federated Learning for Climate Modelling',
    company: 'ClimateAI Zurich',
    companyInitial: 'C',
    score: 91,
    tags: ['Federated ML', 'Python', 'Climate'],
    matchReason: 'Matches your ML depth + sustainability interest',
    summary:
      'Research and implement a federated learning architecture that allows distributed climate stations to collaboratively train predictive models without sharing raw data. You will work with PyTorch, FLOWER framework, and contribute to open-source tooling.',
    contact: 'Prof. Lars Bauer · l.bauer@climateai.ch',
  },
  {
    id: '3',
    title: 'NLP Platform for Academic Research Discovery',
    company: 'studyond',
    companyInitial: 'S',
    score: 87,
    tags: ['NLP', 'Python', 'Data Science'],
    matchReason: 'Matches your Data Science skills + AI tooling focus',
    summary:
      'Build the semantic search backbone of studyond\'s thesis-matching engine. Design embedding pipelines (sentence-transformers), fine-tune retrieval models on academic corpora, and ship a production REST API used by thousands of students across DACH universities.',
    contact: 'Micha Brugger · m.brugger@studyond.com',
  },
]