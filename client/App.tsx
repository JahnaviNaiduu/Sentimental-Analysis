
import React, { useState, useMemo, useCallback } from 'react';
import { Post, AnalysisResults } from './types';
import useFetchData from './hooks/useFetchData';
import api from './services/api';

import Loader from './components/Loader';
import SearchBar from './components/SearchBar';
import PostCard from './components/PostCard';
import AnalysisDialog from './components/AnalysisDialog';

const App: React.FC = () => {
  const { data: posts, loading, error: fetchError } = useFetchData<Post[]>('/get_data_pool');
  const [searchTerm, setSearchTerm] = useState('');
  
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResults | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  const filteredPosts = useMemo(() => {
    if (!posts) return [];
    return posts.filter(post =>
      post.Title.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [posts, searchTerm]);

  const handleAnalyze = useCallback(async (url: string) => {
    setIsDialogOpen(true);
    setIsAnalyzing(true);
    setAnalysisError(null);
    setAnalysisResult(null);

    try {
      const response = await api.post('/perform_analysis', { url });
      setAnalysisResult(response.data.results);
    } catch (err) {
      setAnalysisError('Failed to perform analysis. Please try again.');
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  }, []);

  const handleCloseDialog = useCallback(() => {
    setIsDialogOpen(false);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">
            Social Media Dashboard
          </h1>
          <p className="text-gray-500 mt-1">Explore and analyze the latest posts.</p>
        </div>
      </header>

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <SearchBar onSearchChange={setSearchTerm} />

        {loading && <Loader />}
        {fetchError && <div className="text-center text-red-500 bg-red-100 p-4 rounded-lg">{fetchError}</div>}
        
        {!loading && !fetchError && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredPosts.map((post) => (
              <PostCard key={post.URL} post={post} onAnalyze={handleAnalyze} />
            ))}
          </div>
        )}
      </main>

      <AnalysisDialog 
        isOpen={isDialogOpen} 
        onClose={handleCloseDialog}
        analysisData={analysisResult}
        isLoading={isAnalyzing}
        error={analysisError}
      />
    </div>
  );
};

export default App;
