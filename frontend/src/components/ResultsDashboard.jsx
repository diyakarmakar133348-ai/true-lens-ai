import React, { useState } from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

const ResultsDashboard = ({ report }) => {
  const [activeTab, setActiveTab] = useState('visual');
  if (!report) return null;

  const { 
    verdict, confidence, color, 
    heatmap, waveform, timeline, 
    model_used, details, text_sample, 
    metadata, dimensions, ela_stats, risk_areas, doc_warnings 
  } = report;

  const isVideo = timeline && timeline.length > 0;
  const isAudio = waveform && !heatmap;
  const isDoc = text_sample && !heatmap && !waveform && !timeline;
  const isImage = heatmap && !isVideo;

  return (
    <div className="w-full max-w-5xl mx-auto mt-10 space-y-6 animate-fadeIn">
      
      {/* Top Verdict Banner */}
      <div className={`p-6 rounded-2xl border-l-8 ${color === 'red' ? 'border-red-accent bg-red-500/10' : color === 'yellow' ? 'border-yellow-400 bg-yellow-500/10' : 'border-green-accent bg-green-500/10'} glass-card`}>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <h2 className={`text-3xl font-bold ${color === 'red' ? 'text-red-accent' : color === 'yellow' ? 'text-yellow-400' : 'text-green-accent'}`}>
              {verdict}
            </h2>
            <p className="text-gray-300 mt-1 text-sm">
              Confidence: <span className="font-mono font-bold">{confidence}%</span>
            </p>
            {model_used && (
              <p className="text-xs text-cyan-400 mt-1">🤖 AI Fingerprint: {model_used}</p>
            )}
            {/* Display Image Dimensions if available */}
            {dimensions && (
              <p className="text-xs text-gray-400 mt-1">📐 {dimensions}</p>
            )}
          </div>
          <div className="w-16 h-16">
            <CircularProgressbar
              value={confidence}
              text={`${Math.round(confidence)}%`}
              styles={buildStyles({
                textColor: color === 'red' ? '#ff4d6d' : color === 'yellow' ? '#fbbf24' : '#00c9a7',
                pathColor: color === 'red' ? '#ff4d6d' : color === 'yellow' ? '#fbbf24' : '#00c9a7',
                trailColor: '#1e293b',
                textSize: '28px',
              })}
            />
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex flex-wrap border-b border-gray-700/50 space-x-4 px-2">
        <button onClick={() => setActiveTab('visual')} className={`py-3 px-1 text-sm font-medium transition ${activeTab === 'visual' ? 'border-b-2 border-cyan text-cyan' : 'text-gray-400 hover:text-gray-200'}`}>
          {isAudio ? '🎵 Waveform' : isVideo ? '⏳ Timeline' : isDoc ? '📄 Content' : '🔍 Visual'}
        </button>
        <button onClick={() => setActiveTab('summary')} className={`py-3 px-1 text-sm font-medium transition ${activeTab === 'summary' ? 'border-b-2 border-cyan text-cyan' : 'text-gray-400 hover:text-gray-200'}`}>
          🧠 Analysis
        </button>
        <button onClick={() => setActiveTab('metadata')} className={`py-3 px-1 text-sm font-medium transition ${activeTab === 'metadata' ? 'border-b-2 border-cyan text-cyan' : 'text-gray-400 hover:text-gray-200'}`}>
          📊 Metadata
        </button>
      </div>

      {/* Tab Content */}
      <div className="p-4 bg-dark-card/50 rounded-2xl border border-gray-700/20 min-h-[300px]">
        
        {activeTab === 'visual' && (
          <div>
            {isAudio && waveform && (
              <div>
                <h4 className="text-sm font-semibold text-gray-400 mb-2">🎵 Audio Waveform</h4>
                <img src={waveform} alt="Waveform" className="w-full rounded-xl border border-gray-700" />
              </div>
            )}
            
            {isVideo && timeline && (
              <div>
                <h4 className="text-sm font-semibold text-gray-400 mb-2">⏳ Video Timeline</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {timeline.map((item, idx) => (
                    <div key={idx} className={`p-3 rounded-xl border ${item.status === 'Red' ? 'border-red-accent bg-red-500/10' : 'border-green-accent bg-green-500/10'}`}>
                      <p className="text-xs text-gray-400">{item.timestamp}</p>
                      <p className="text-sm font-semibold">{item.status === 'Red' ? '⚠️ Fake' : '✅ Real'}</p>
                      <p className="text-xs text-gray-500">{item.label}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {isDoc && text_sample && (
              <div>
                <h4 className="text-sm font-semibold text-gray-400 mb-2">📄 Extracted Text</h4>
                <div className="p-4 bg-navy/60 rounded-xl border border-gray-700 text-gray-300 text-sm">
                  "{text_sample}"
                </div>
                {doc_warnings && doc_warnings.length > 0 && (
                  <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded text-red-300 text-xs">
                    ⚠️ {doc_warnings.join(' | ')}
                  </div>
                )}
              </div>
            )}

            {isImage && heatmap && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">🔍 Forensic Heatmap</h4>
                  <img src={heatmap} alt="Heatmap" className="w-full rounded-xl border border-gray-700" />
                </div>
                <div>
                  <h4 className="text-sm font-semibold text-gray-400 mb-2">📊 Image Forensics</h4>
                  <ul className="space-y-2 text-sm bg-navy/40 p-3 rounded-xl border border-gray-700">
                    <li className="flex justify-between"><span className="text-gray-400">ELA Stats</span><span className="font-mono text-white">{ela_stats || 'N/A'}</span></li>
                    <li className="flex justify-between"><span className="text-gray-400">Risk Areas</span><span className={`font-mono ${risk_areas && risk_areas !== 'Uniform compression' ? 'text-red-400' : 'text-green-400'}`}>{risk_areas || 'N/A'}</span></li>
                    <li className="flex justify-between"><span className="text-gray-400">Dimensions</span><span className="font-mono text-white">{dimensions || 'N/A'}</span></li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'summary' && (
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-gray-400">🧠 AI Explanation</h4>
            <div className="p-4 bg-navy/40 rounded-xl border border-gray-700/30 text-gray-200 leading-relaxed whitespace-pre-wrap">
              {details || "Analysis complete."}
            </div>
          </div>
        )}

        {activeTab === 'metadata' && (
          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-gray-400 mb-3">📄 File & System Data</h4>
            {metadata && Object.entries(metadata).map(([key, value]) => (
              <div key={key} className="flex flex-wrap justify-between p-2 border-b border-gray-700/30">
                <span className="text-gray-400 text-sm capitalize">{key.replace('_', ' ')}</span>
                <span className="text-white text-sm font-mono truncate max-w-[200px]">{String(value)}</span>
              </div>
            ))}
            <div className="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded text-xs text-yellow-300">
              ⚡ Files are encrypted and auto-deleted after 24 hours.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsDashboard;