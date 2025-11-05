
export interface Post {
  Category: string;
  Date: string;
  Title: string;
  URL: string;
  Keywords: string;
  Description: string;
}

export interface AnalysisResults {
  polarity: number;
  subjectivity: number;
  word_count: number;
  complex_words: number;
  syllable_per_word: number;
  personal_pronouns: number;
}
