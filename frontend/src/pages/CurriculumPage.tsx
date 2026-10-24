import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { curriculumApi, SkillPrerequisitesResponse } from '../api/curriculum';
import { Domain, Skill, Topic, Subtopic } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorBanner } from '../components/ErrorBanner';
import {
  BookOpen,
  GitBranch,
  Layers,
  ChevronRight,
  Sparkles,
  ArrowRight,
  Info,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

export const CurriculumPage: React.FC = () => {
  const navigate = useNavigate();
  const [domains, setDomains] = useState<Domain[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<Domain | null>(null);
  const [hierarchy, setHierarchy] = useState<Domain | null>(null);
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);
  const [prereqs, setPrereqs] = useState<SkillPrerequisitesResponse | null>(null);

  const [loadingDomains, setLoadingDomains] = useState(true);
  const [loadingHierarchy, setLoadingHierarchy] = useState(false);
  const [loadingPrereqs, setLoadingPrereqs] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDomains = async () => {
      try {
        setLoadingDomains(true);
        setError(null);
        const data = await curriculumApi.getDomains();
        setDomains(data);
        if (data.length > 0) {
          handleSelectDomain(data[0]);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load curriculum domains.');
      } finally {
        setLoadingDomains(false);
      }
    };
    fetchDomains();
  }, []);

  const handleSelectDomain = async (domain: Domain) => {
    setSelectedDomain(domain);
    setSelectedSkill(null);
    setPrereqs(null);
    try {
      setLoadingHierarchy(true);
      const data = await curriculumApi.getDomainHierarchy(domain.id);
      setHierarchy(data);
    } catch (err: any) {
      setError(err.message || `Failed to load hierarchy for ${domain.name}`);
    } finally {
      setLoadingHierarchy(false);
    }
  };

  const handleSelectSkill = async (skill: Skill) => {
    setSelectedSkill(skill);
    try {
      setLoadingPrereqs(true);
      const prereqData = await curriculumApi.getSkillPrerequisites(skill.id);
      setPrereqs(prereqData);
    } catch (err: any) {
      console.warn('Prerequisite load error:', err);
    } finally {
      setLoadingPrereqs(false);
    }
  };

  if (loadingDomains) {
    return <LoadingSpinner message="Loading curriculum knowledge graph..." />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Curriculum & Skill Dependency Graph</h1>
        <p className="text-sm text-slate-500 mt-1">
          Explore all 11 placement domains, topological prerequisites, and Bloom cognitive taxonomy
        </p>
      </div>

      {error && <ErrorBanner message={error} />}

      {/* 11 Domains Pill Selector */}
      <div className="flex overflow-x-auto pb-2 gap-2 scrollbar-thin">
        {domains.map((dom) => {
          const isSelected = selectedDomain?.id === dom.id;
          return (
            <button
              key={dom.id}
              onClick={() => handleSelectDomain(dom)}
              className={`flex-shrink-0 px-3.5 py-2 rounded-xl text-xs font-semibold transition flex items-center space-x-2 border ${
                isSelected
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                  : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
              }`}
            >
              <span>{dom.name}</span>
              <span
                className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                  isSelected ? 'bg-indigo-700 text-white' : 'bg-slate-100 text-slate-500'
                }`}
              >
                {dom.skill_count}
              </span>
            </button>
          );
        })}
      </div>

      {/* Domain Content & Prerequisite Inspector Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Topics & Skills Breakdown */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
            <div className="flex items-start justify-between pb-4 border-b border-slate-100">
              <div>
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
                  Domain Code: {selectedDomain?.code}
                </span>
                <h2 className="text-xl font-bold text-slate-900 mt-0.5">{selectedDomain?.name}</h2>
                <p className="text-xs text-slate-500 mt-1">{selectedDomain?.description}</p>
              </div>
            </div>

            {loadingHierarchy ? (
              <LoadingSpinner message="Loading domain topics..." />
            ) : hierarchy && hierarchy.topics && hierarchy.topics.length > 0 ? (
              <div className="mt-6 space-y-6">
                {hierarchy.topics.map((topic: Topic) => (
                  <div key={topic.id} className="border border-slate-200 rounded-xl p-4 bg-slate-50/50">
                    <div className="flex items-center justify-between pb-2 mb-3 border-b border-slate-200">
                      <h3 className="text-sm font-bold text-slate-900 flex items-center">
                        <Layers className="w-4 h-4 mr-2 text-indigo-500" />
                        {topic.name}
                      </h3>
                      <button
                        onClick={() =>
                          navigate('/assessment', {
                            state: { domainId: selectedDomain?.id, topicId: topic.id },
                          })
                        }
                        className="inline-flex items-center px-3 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-semibold text-xs rounded-lg border border-indigo-200 transition"
                      >
                        Practice Topic
                        <ArrowRight className="w-3.5 h-3.5 ml-1" />
                      </button>
                    </div>

                    <div className="mt-3 space-y-3 pl-2">
                      {topic.subtopics.map((subtopic: Subtopic) => (
                        <div key={subtopic.id} className="space-y-1.5">
                          <span className="text-xs font-semibold text-slate-600">{subtopic.name}</span>
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1">
                            {subtopic.skills.map((skill: Skill) => {
                              const isSkillActive = selectedSkill?.id === skill.id;
                              return (
                                <button
                                  key={skill.id}
                                  onClick={() => handleSelectSkill(skill)}
                                  className={`text-left p-2.5 rounded-lg border text-xs transition flex items-center justify-between group ${
                                    isSkillActive
                                      ? 'bg-indigo-50 border-indigo-300 text-indigo-900'
                                      : 'bg-white border-slate-200 hover:border-slate-300 text-slate-700'
                                  }`}
                                >
                                  <div>
                                    <div className="font-medium group-hover:text-indigo-600 transition">
                                      {skill.name}
                                    </div>
                                    <div className="text-[10px] text-slate-400 mt-0.5">
                                      Difficulty: {skill.difficulty_target?.toFixed(2)} • {skill.bloom_level}
                                    </div>
                                  </div>
                                  <ChevronRight className="w-3.5 h-3.5 text-slate-300 group-hover:text-indigo-500" />
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 py-8 text-center">No subtopics available for this domain.</p>
            )}
          </div>
        </div>

        {/* Right Col: Skill Prerequisite Chain Inspector */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm sticky top-24">
            <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-indigo-600 mb-2">
              <GitBranch className="w-4 h-4" />
              <span>DAG Prerequisite Analysis</span>
            </div>

            {selectedSkill ? (
              <div className="space-y-5">
                <div>
                  <h3 className="text-base font-bold text-slate-900">{selectedSkill.name}</h3>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="text-[10px] bg-slate-100 text-slate-600 font-mono px-2 py-0.5 rounded">
                      {selectedSkill.code}
                    </span>
                    <span className="text-[10px] bg-indigo-50 text-indigo-700 font-semibold px-2 py-0.5 rounded">
                      Bloom: {selectedSkill.bloom_level}
                    </span>
                  </div>
                </div>

                {loadingPrereqs ? (
                  <LoadingSpinner message="Checking Kahn topological order..." />
                ) : prereqs ? (
                  <div className="space-y-4 text-xs">
                    {/* Direct Prerequisites */}
                    <div>
                      <span className="font-semibold text-slate-700 block mb-1.5">
                        Direct Prerequisites:
                      </span>
                      {prereqs.direct_prerequisites.length > 0 ? (
                        <div className="space-y-1">
                          {prereqs.direct_prerequisites.map((p) => (
                            <div
                              key={p.id}
                              className="p-2 bg-slate-50 rounded border border-slate-100 flex items-center justify-between"
                            >
                              <span className="font-medium text-slate-800">{p.name}</span>
                              <span className="text-[10px] text-slate-400">Diff: {p.difficulty_level}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="p-2 bg-emerald-50 text-emerald-800 rounded text-[11px] flex items-center">
                          <CheckCircle2 className="w-3.5 h-3.5 mr-1.5 text-emerald-600" />
                          Foundational Concept (Zero prerequisites required)
                        </div>
                      )}
                    </div>

                    {/* Foundational Topological Ancestors */}
                    {prereqs.foundational_prerequisites_topological.length > prereqs.direct_prerequisites.length && (
                      <div>
                        <span className="font-semibold text-slate-700 block mb-1.5">
                          Complete Prerequisite Chain (Topological):
                        </span>
                        <div className="space-y-1">
                          {prereqs.foundational_prerequisites_topological.map((p) => (
                            <div key={p.id} className="p-1.5 bg-slate-50 rounded text-slate-600 text-[11px]">
                              • {p.name}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Downstream Dependents */}
                    <div>
                      <span className="font-semibold text-slate-700 block mb-1.5">
                        Unlocks Downstream Skills:
                      </span>
                      {prereqs.direct_dependents.length > 0 ? (
                        <div className="space-y-1">
                          {prereqs.direct_dependents.map((d) => (
                            <div key={d.id} className="p-2 bg-indigo-50/50 rounded border border-indigo-100 text-indigo-900 font-medium">
                              {d.name}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-slate-400 text-[11px]">No further downstream skills depending on this node.</p>
                      )}
                    </div>

                    {/* Action buttons */}
                    <div className="pt-3 border-t border-slate-100 space-y-2">
                      <button
                        onClick={() => navigate('/tutor', { state: { skillId: selectedSkill.id } })}
                        className="w-full flex items-center justify-center py-2 px-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold transition"
                      >
                        <Sparkles className="w-3.5 h-3.5 mr-1.5" /> Ask Socratic AI Tutor on this Skill
                      </button>
                      <button
                        onClick={() => navigate('/assessment', { state: { domainId: selectedDomain?.id } })}
                        className="w-full flex items-center justify-center py-2 px-3 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold transition"
                      >
                        Practice this Domain <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                      </button>
                    </div>
                  </div>
                ) : null}
              </div>
            ) : (
              <div className="py-8 text-center text-xs text-slate-500">
                <Info className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                Select any skill from the list on the left to inspect its dependency ancestors and unlocked skills.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
