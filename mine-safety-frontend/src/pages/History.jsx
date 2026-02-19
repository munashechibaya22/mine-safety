import React, { useEffect, useMemo, useState } from 'react';
import api from '../api/axios';
import { CheckCircle2, XCircle, Archive } from 'lucide-react';

const parseItems = (value) => {
  if (!value) return [];

  try {
    const parsed = typeof value === 'string' ? JSON.parse(value) : value;
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
};

const History = () => {
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await api.get('/detections');
      setDetections(response.data);
    } catch (error) {
      console.error('Failed to fetch history:', error);
      setDetections([]);
    } finally {
      setLoading(false);
    }
  };

  const acceptedCount = useMemo(() => detections.filter((detection) => detection.is_safe).length, [detections]);
  const deniedCount = detections.length - acceptedCount;

  if (loading) {
    return (
      <div className="soft-card p-10 text-center" style={{ borderRadius: '8px' }}>
        <p className="text-sm font-medium text-slate-500">Loading detection history...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="glass-panel p-6 sm:p-8" style={{ borderRadius: '8px' }}>
        <p className="text-xs font-semibold uppercase tracking-[0.15em] text-blue-600">Audit Trail</p>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-900">Detection History</h1>
        <p className="mt-2 max-w-2xl text-sm text-slate-600">
          Browse historical PPE decisions with timestamps, detected items, and denial reasons.
        </p>
      </section>

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <article className="soft-card p-5" style={{ borderRadius: '8px' }}>
          <p className="text-sm font-semibold text-slate-500">Total Records</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{detections.length}</p>
        </article>
        <article className="soft-card p-5" style={{ borderRadius: '8px' }}>
          <p className="text-sm font-semibold text-emerald-600">Accepted</p>
          <p className="mt-2 text-3xl font-bold text-emerald-700">{acceptedCount}</p>
        </article>
        <article className="soft-card p-5" style={{ borderRadius: '8px' }}>
          <p className="text-sm font-semibold text-orange-600">Denied</p>
          <p className="mt-2 text-3xl font-bold text-orange-700">{deniedCount}</p>
        </article>
      </section>

      <section className="soft-card overflow-hidden" style={{ borderRadius: '8px' }}>
        <div className="border-b border-blue-100 px-5 py-4 sm:px-6">
          <h2 className="text-lg font-bold text-slate-900">All Detections</h2>
          <p className="text-sm text-slate-500">Chronological log of every scanned file and decision.</p>
        </div>

        {detections.length === 0 ? (
          <div className="px-6 py-14 text-center">
            <Archive className="mx-auto h-10 w-10 text-blue-400" />
            <p className="mt-3 text-sm font-semibold text-slate-700">No detections yet</p>
            <p className="mt-1 text-xs text-slate-500">Run your first safety scan from the Detection page.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-blue-50 text-xs uppercase tracking-wide text-slate-500">
                <tr>
                  <th className="px-6 py-3 text-left font-semibold">Date & Time</th>
                  <th className="px-6 py-3 text-left font-semibold">Type</th>
                  <th className="px-6 py-3 text-left font-semibold">Status</th>
                  <th className="px-6 py-3 text-left font-semibold">Confidence</th>
                  <th className="px-6 py-3 text-left font-semibold">Detected Items</th>
                  <th className="px-6 py-3 text-left font-semibold">Missing Items</th>
                  <th className="px-6 py-3 text-left font-semibold">Reason</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-blue-50 bg-white">
                {detections.map((detection) => {
                  const detectedItems = parseItems(detection.detected_items);
                  const missingItems = parseItems(detection.missing_items);

                  return (
                    <tr key={detection.id} className="hover:bg-blue-50/40">
                      <td className="px-6 py-4 whitespace-nowrap text-slate-700">
                        {new Date(detection.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap capitalize text-slate-700">{detection.file_type}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2">
                          {detection.is_safe ? (
                            <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                          ) : (
                            <XCircle className="h-4 w-4 text-orange-600" />
                          )}
                          <span
                            className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${
                              detection.is_safe ? 'bg-emerald-100 text-emerald-700' : 'bg-orange-100 text-orange-700'
                            }`}
                          >
                            {detection.is_safe ? 'Accepted' : 'Denied'}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap font-semibold text-slate-700">{detection.confidence}%</td>
                      <td className="px-6 py-4">
                        {detectedItems.length > 0 ? (
                          <div className="flex flex-wrap gap-1.5">
                            {detectedItems.map((item, index) => (
                              <span
                                key={`${item}-${index}`}
                                className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold text-emerald-700"
                              >
                                {item}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span className="text-xs text-slate-500">None</span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        {missingItems.length > 0 ? (
                          <div className="flex flex-wrap gap-1.5">
                            {missingItems.map((item, index) => (
                              <span
                                key={`${item}-${index}`}
                                className="rounded-full bg-orange-100 px-2.5 py-1 text-xs font-semibold text-orange-700"
                              >
                                {item}
                              </span>
                            ))}
                          </div>
                        ) : (
                          <span className="text-xs text-slate-500">None</span>
                        )}
                      </td>
                      <td className="max-w-sm px-6 py-4 text-slate-600">{detection.reason}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
};

export default History;
