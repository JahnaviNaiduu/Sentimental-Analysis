
import React from 'react';
import { Post } from '../types';

interface PostCardProps {
  post: Post;
  onAnalyze: (url: string) => void;
}

const isImageUrl = (url: string): boolean => {
    return /\.(jpg|jpeg|png|gif)$/i.test(url);
}

const PostCard: React.FC<PostCardProps> = ({ post, onAnalyze }) => {
  const hasImage = isImageUrl(post.URL);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 ease-in-out group flex flex-col">
      {hasImage && (
        <div className="relative h-48 w-full">
            <img src={post.URL} alt={post.Title} className="object-cover h-full w-full" />
        </div>
      )}
      
      <div className="p-4 flex flex-col flex-grow">
        <p className="text-xs font-semibold text-blue-600 uppercase tracking-wide">{post.Category}</p>
        <h3 className="text-lg font-bold mt-1 text-gray-900 leading-tight">{post.Title}</h3>
        <p className="text-sm text-gray-500 mt-1">{new Date(post.Date).toLocaleDateString()}</p>
        <p className="text-sm text-gray-700 mt-2 flex-grow">{post.Description}</p>
        
        <div className="mt-4">
          <p className="text-xs text-gray-500">Keywords: <span className="font-medium text-gray-600">{post.Keywords}</span></p>
        </div>
      </div>

      <div className="p-4 pt-0">
          <button 
            onClick={() => onAnalyze(post.URL)}
            className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Analyze
          </button>
      </div>
    </div>
  );
};

export default PostCard;
