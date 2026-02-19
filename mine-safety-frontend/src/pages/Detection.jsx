import React, { useCallback, useEffect, useRef, useState } from 'react';
import api from '../api/axios';
import {
  Upload,
  Camera,
  CheckCircle2,
  XCircle,
  Loader2,
  RotateCcw,
  ScanLine,
} from 'lucide-react';

const parseItems = (value) => {
  if (!value) return [];

  try {
    const parsed = typeof value === 'string' ? JSON.parse(value) : value;
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
};

const Detection = () => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [useCamera, setUseCamera] = useState(false);

  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const fileInputRef = useRef(null);

  const updatePreview = (url) => {
    setPreview((current) => {
      if (current) URL.revokeObjectURL(current);
      return url;
    });
  };

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setUseCamera(false);
  }, []);

  useEffect(() => {
    return () => {
      stopCamera();
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview, stopCamera]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    stopCamera();
    setFile(selectedFile);
    updatePreview(URL.createObjectURL(selectedFile));
    setResult(null);
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      streamRef.current = stream;
      setUseCamera(true);
      setResult(null);
    } catch {
      alert('Failed to access camera');
    }
  };

  const capturePhoto = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.drawImage(video, 0, 0);

    canvas.toBlob((blob) => {
      if (!blob) {
        alert('Failed to capture image');
        return;
      }

      const capturedFile = new File([blob], `capture-${Date.now()}.jpg`, { type: 'image/jpeg' });
      setFile(capturedFile);
      updatePreview(URL.createObjectURL(capturedFile));
      stopCamera();
    }, 'image/jpeg');
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (error) {
      alert(`Detection failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    stopCamera();
    setFile(null);
    setResult(null);
    updatePreview(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const isVideo = file?.type?.startsWith('video/');
  const detectedItems = parseItems(result?.detected_items);
  const missingItems = parseItems(result?.missing_items);

  return (
    <div className="space-y-6">
      <section className="glass-panel p-6 sm:p-8" style={{ borderRadius: '8px' }}>
        <p className="text-xs font-semibold uppercase tracking-[0.15em] text-blue-600">Safety Scan</p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">Analyze Worker Media</h1>
        <p className="mt-2 max-w-2xl text-sm text-slate-600">
          Upload an image/video or capture a camera frame to verify mandatory safety equipment.
        </p>
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[1fr_1.3fr]">
        <article className="soft-card p-5 sm:p-6" style={{ borderRadius: '8px' }}>
          <h2 className="text-lg font-bold text-slate-900">Input Source</h2>
          <p className="mt-1 text-sm text-slate-500">Choose how you want to run a PPE detection scan.</p>

          <div className="mt-5 flex flex-wrap gap-3">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
            >
              <Upload className="h-4 w-4" />
              Upload File
            </button>
            <button
              onClick={useCamera ? stopCamera : startCamera}
              className={`inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold text-white transition ${
                useCamera ? 'bg-orange-500 hover:bg-orange-600' : 'bg-slate-700 hover:bg-slate-800'
              }`}
            >
              <Camera className="h-4 w-4" />
              {useCamera ? 'Stop Camera' : 'Use Camera'}
            </button>
            {file && !result && (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="inline-flex items-center gap-2 rounded-lg bg-blue-500 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <ScanLine className="h-4 w-4" />}
                Analyze
              </button>
            )}
            {(file || result || useCamera) && (
              <button
                onClick={reset}
                className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
              >
                <RotateCcw className="h-4 w-4" />
                Reset
              </button>
            )}
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,video/*"
            onChange={handleFileChange}
            className="hidden"
          />

          {useCamera && (
            <div className="mt-5 space-y-3 border border-blue-100 bg-blue-50/60 p-4" style={{ borderRadius: '8px' }}>
              <video ref={videoRef} autoPlay className="w-full border border-blue-200 bg-slate-900" style={{ borderRadius: '8px' }} />
              <button
                onClick={capturePhoto}
                className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700"
              >
                <Camera className="h-4 w-4" />
                Capture Photo
              </button>
            </div>
          )}

          <canvas ref={canvasRef} className="hidden" />
        </article>

        <article className="soft-card p-5 sm:p-6" style={{ borderRadius: '8px' }}>
          <h2 className="text-lg font-bold text-slate-900">Preview</h2>
          <p className="mt-1 text-sm text-slate-500">Confirm the selected media before running analysis.</p>

          <div className="mt-5">
            {preview && !useCamera ? (
              isVideo ? (
                <video src={preview} controls className="w-full border border-blue-100 bg-slate-900" style={{ borderRadius: '8px' }} />
              ) : (
                <img src={preview} alt="Preview" className="w-full border border-blue-100 object-cover" style={{ borderRadius: '8px' }} />
              )
            ) : (
              <div className="border border-dashed border-blue-200 bg-blue-50 px-4 py-14 text-center" style={{ borderRadius: '8px' }}>
                <p className="text-sm font-medium text-slate-600">No media selected yet.</p>
                <p className="mt-1 text-xs text-slate-500">Upload a file or capture a camera frame to start.</p>
              </div>
            )}
          </div>
        </article>
      </section>

      {result && (
        <section
          className={`border p-6 ${
            result.is_safe ? 'border-emerald-200 bg-emerald-50/70' : 'border-orange-200 bg-orange-50/70'
          }`}
          style={{ borderRadius: '8px' }}
        >
          <div className="flex flex-wrap items-center gap-4">
            <span
              className={`inline-flex h-12 w-12 items-center justify-center ${
                result.is_safe ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'
              }`}
              style={{ borderRadius: '8px' }}
            >
              {result.is_safe ? <CheckCircle2 className="h-7 w-7" /> : <XCircle className="h-7 w-7" />}
            </span>
            <div>
              <h3 className="text-2xl font-bold text-slate-900">
                {result.is_safe ? 'Entry Approved' : 'Entry Denied'}
              </h3>
              <p className="text-sm text-slate-600">Confidence score: {result.confidence}%</p>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
            <div className="border border-white/70 bg-white/80 p-4" style={{ borderRadius: '8px' }}>
              <h4 className="text-sm font-semibold text-slate-700">Reason</h4>
              <p className="mt-2 text-sm text-slate-600">{result.reason}</p>
            </div>

            <div className="border border-white/70 bg-white/80 p-4" style={{ borderRadius: '8px' }}>
              <h4 className="text-sm font-semibold text-slate-700">Detected Equipment</h4>
              {detectedItems.length > 0 ? (
                <div className="mt-2 flex flex-wrap gap-2">
                  {detectedItems.map((item, index) => (
                    <span key={`${item}-${index}`} className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
                      {item}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="mt-2 text-sm text-slate-500">No detected equipment listed.</p>
              )}
            </div>
          </div>

          <div className="mt-4 border border-white/70 bg-white/80 p-4" style={{ borderRadius: '8px' }}>
            <h4 className="text-sm font-semibold text-slate-700">Missing Equipment</h4>
            {missingItems.length > 0 ? (
              <div className="mt-2 flex flex-wrap gap-2">
                {missingItems.map((item, index) => (
                  <span key={`${item}-${index}`} className="rounded-full bg-orange-100 px-3 py-1 text-xs font-semibold text-orange-700">
                    {item}
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-2 text-sm text-slate-500">No missing equipment detected.</p>
            )}
          </div>
        </section>
      )}
    </div>
  );
};

export default Detection;
