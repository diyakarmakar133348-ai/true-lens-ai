import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiFile, FiX, FiVideo, FiMusic, FiImage, FiFileText } from 'react-icons/fi';

const UploadArea = ({ onUpload, isLoading }) => {
  const [file, setFile] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const selected = acceptedFiles[0];
    if (selected) {
      setFile(selected);
      onUpload(selected);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.png', '.jpg', '.webp'],
      'video/*': ['.mp4', '.mov', '.avi', '.mkv'],
      'audio/*': ['.mp3', '.wav', '.m4a'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    disabled: isLoading,
  });

  const getFileIcon = () => {
    const ext = file?.name?.split('.').pop()?.toLowerCase();
    if (['jpg', 'jpeg', 'png', 'webp'].includes(ext)) return <FiImage className="text-cyan w-6 h-6" />;
    if (['mp4', 'mov', 'avi', 'mkv'].includes(ext)) return <FiVideo className="text-purple-400 w-6 h-6" />;
    if (['mp3', 'wav', 'm4a'].includes(ext)) return <FiMusic className="text-green-400 w-6 h-6" />;
    if (['pdf', 'docx'].includes(ext)) return <FiFileText className="text-yellow-400 w-6 h-6" />;
    return <FiFile className="text-gray-400 w-6 h-6" />;
  };

  const getTypeLabel = () => {
    const ext = file?.name?.split('.').pop()?.toLowerCase();
    if (['jpg', 'jpeg', 'png', 'webp'].includes(ext)) return '📷 Image';
    if (['mp4', 'mov', 'avi', 'mkv'].includes(ext)) return '🎬 Video';
    if (['mp3', 'wav', 'm4a'].includes(ext)) return '🎵 Audio';
    if (['pdf', 'docx'].includes(ext)) return '📄 Document';
    return '📎 File';
  };

  return (
    <div
      {...getRootProps()}
      className={`
        relative w-full max-w-2xl mx-auto p-8 border-2 border-dashed rounded-2xl transition-all duration-300
        ${isDragActive 
          ? 'border-cyan bg-cyan/10 scale-[1.02]' 
          : 'border-gray-600 hover:border-cyan/50 hover:bg-navy/50'
        }
        ${isLoading ? 'opacity-50 pointer-events-none' : 'cursor-pointer'}
        glass-card
      `}
    >
      <input {...getInputProps()} />
      
      {!file ? (
        <div className="text-center py-8">
          <FiUploadCloud className="w-16 h-16 text-cyan mx-auto mb-4" />
          <p className="text-xl font-semibold text-white">
            {isDragActive ? 'Drop your file here' : 'Upload any file to scan'}
          </p>
          <p className="text-sm text-gray-400 mt-2">
            Drag & drop or click to browse • Supports Images, Videos, Audio, PDFs & DOCX
          </p>
          <div className="flex flex-wrap justify-center gap-2 mt-4 text-xs text-gray-500">
            <span className="px-3 py-1 bg-navy/50 rounded-full border border-gray-700">🖼️ JPG/PNG</span>
            <span className="px-3 py-1 bg-navy/50 rounded-full border border-gray-700">🎬 MP4/MOV</span>
            <span className="px-3 py-1 bg-navy/50 rounded-full border border-gray-700">🎵 MP3/WAV</span>
            <span className="px-3 py-1 bg-navy/50 rounded-full border border-gray-700">📄 PDF/DOCX</span>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-between p-3 bg-navy/60 rounded-xl border border-cyan/20">
          <div className="flex items-center gap-3">
            {getFileIcon()}
            <div>
              <p className="text-sm font-medium text-white truncate max-w-[200px]">{file.name}</p>
              <p className="text-xs text-gray-400">{getTypeLabel()} • {(file.size / 1024).toFixed(1)} KB</p>
            </div>
          </div>
          <button
            onClick={(e) => { e.stopPropagation(); setFile(null); }}
            className="p-1 hover:bg-red-500/20 rounded-full transition"
            disabled={isLoading}
          >
            <FiX className="text-red-400 w-5 h-5" />
          </button>
        </div>
      )}
    </div>
  );
};

export default UploadArea;