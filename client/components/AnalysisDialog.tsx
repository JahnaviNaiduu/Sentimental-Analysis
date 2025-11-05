
import React, { useMemo } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from 'recharts';
import { AnalysisResults } from '../types';

interface AnalysisDialogProps {
  isOpen: boolean;
  onClose: () => void;
  analysisData: AnalysisResults | null;
  isLoading: boolean;
  error: string | null;
}

const AnalysisDialog: React.FC<AnalysisDialogProps> = ({ isOpen, onClose, analysisData, isLoading, error }) => {

  const chartData = useMemo(() => {
    if (!analysisData) return [];
    return [
      { name: 'Polarity', value: analysisData.polarity.toFixed(2) },
      { name: 'Subjectivity', value: analysisData.subjectivity.toFixed(2) },
      { name: 'Word Count', value: analysisData.word_count },
      { name: 'Complex Words', value: analysisData.complex_words },
      { name: 'Syllables/Word', value: analysisData.syllable_per_word.toFixed(2) },
      { name: 'Pronouns', value: analysisData.personal_pronouns },
    ];
  }, [analysisData]);

  const backdropVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  };

  const dialogVariants = {
    hidden: { x: '100%' },
    visible: { x: 0 },
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="fixed inset-0 bg-black bg-opacity-50 z-40"
            variants={backdropVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
            onClick={onClose}
            transition={{ duration: 0.3 }}
          />
          <motion.div
            className="fixed top-0 right-0 h-full w-full max-w-lg bg-white shadow-2xl z-50 p-6 flex flex-col"
            variants={dialogVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Sentiment Analysis</h2>
              <button onClick={onClose} className="text-gray-500 hover:text-gray-800 transition-colors">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="flex-grow overflow-y-auto">
              {isLoading && (
                <div className="flex items-center justify-center h-full">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                   <p className="ml-3 text-gray-600">Analyzing content...</p>
                </div>
              )}
              {error && <div className="text-center text-red-500 bg-red-100 p-4 rounded-lg">{error}</div>}
              
              {analysisData && !isLoading && (
                <>
                  <div className="h-64 w-full mb-8">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                        <YAxis />
                        <Tooltip contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }} />
                        <Legend />
                        <Bar dataKey="value" fill="#3b82f6" name="Metric Value" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                      {chartData.map(item => (
                          <div key={item.name} className="bg-gray-100 p-3 rounded-lg">
                              <p className="text-sm text-gray-600">{item.name}</p>
                              <p className="text-lg font-bold text-gray-900">{item.value}</p>
                          </div>
                      ))}
                  </div>
                </>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default AnalysisDialog;
