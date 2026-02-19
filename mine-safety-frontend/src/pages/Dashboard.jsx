import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import { CheckCircle, XCircle, Activity, TrendingUp } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await api.get('/dashboard');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8 text-sm text-gray-600">Loading...</div>;
  }

  const acceptanceRate = stats.total_detections > 0 
    ? Math.round((stats.total_accepted / stats.total_detections) * 100) 
    : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">Plan, prioritize, and accomplish your tasks with ease.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-5 text-white relative overflow-hidden" style={{ borderRadius: '8px' }}>
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-medium opacity-90">Total Detections</p>
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <Activity className="w-4 h-4" />
              </div>
            </div>
            <p className="text-3xl font-bold">{stats.total_detections}</p>
            <p className="text-xs opacity-75 mt-2 flex items-center gap-1">
              <TrendingUp className="w-3 h-3" />
              All time scans
            </p>
          </div>
        </div>

        <div className="bg-white p-5 border border-gray-200" style={{ borderRadius: '8px' }}>
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium text-gray-600">Accepted</p>
            <div className="w-8 h-8 bg-blue-50 rounded-full flex items-center justify-center">
              <CheckCircle className="w-4 h-4 text-blue-600" />
            </div>
          </div>
          <p className="text-3xl font-bold text-gray-900">{stats.total_accepted}</p>
          <p className="text-xs text-gray-500 mt-2">Safe to enter</p>
        </div>

        <div className="bg-white p-5 border border-gray-200" style={{ borderRadius: '8px' }}>
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium text-gray-600">Denied</p>
            <div className="w-8 h-8 bg-orange-50 rounded-full flex items-center justify-center">
              <XCircle className="w-4 h-4 text-orange-600" />
            </div>
          </div>
          <p className="text-3xl font-bold text-gray-900">{stats.total_denied}</p>
          <p className="text-xs text-gray-500 mt-2">Entry blocked</p>
        </div>

        <div className="bg-white p-5 border border-gray-200" style={{ borderRadius: '8px' }}>
          <div className="flex items-center justify-between mb-2">
            <p className="text-sm font-medium text-gray-600">Approval Rate</p>
            <div className="w-8 h-8 bg-blue-50 rounded-full flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-blue-600" />
            </div>
          </div>
          <p className="text-3xl font-bold text-gray-900">{acceptanceRate}%</p>
          <p className="text-xs text-gray-500 mt-2">Success rate</p>
        </div>
      </div>

      {/* Recent Detections Table */}
      <div className="bg-white border border-gray-200 overflow-hidden" style={{ borderRadius: '8px' }}>
        <div className="px-5 py-4 border-b border-gray-200">
          <h2 className="text-base font-semibold text-gray-900">Recent Detections</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-5 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-5 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-5 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-5 py-3 text-left text-xs font-medium text-gray-500 uppercase">Confidence</th>
                <th className="px-5 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats.recent_detections.slice(0, 5).map((detection) => (
                <tr key={detection.id} className="hover:bg-gray-50">
                  <td className="px-5 py-3 whitespace-nowrap text-sm text-gray-900">
                    {new Date(detection.created_at).toLocaleString()}
                  </td>
                  <td className="px-5 py-3 whitespace-nowrap text-sm text-gray-900 capitalize">
                    {detection.file_type}
                  </td>
                  <td className="px-5 py-3 whitespace-nowrap">
                    <span className={`px-2.5 py-1 inline-flex text-xs font-medium ${
                      detection.is_safe ? 'bg-blue-100 text-blue-700' : 'bg-orange-100 text-orange-700'
                    }`} style={{ borderRadius: '8px' }}>
                      {detection.is_safe ? 'Accepted' : 'Denied'}
                    </span>
                  </td>
                  <td className="px-5 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                    {detection.confidence}%
                  </td>
                  <td className="px-5 py-3 text-sm text-gray-600">
                    {detection.reason}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
