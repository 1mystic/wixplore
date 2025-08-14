<template>
  <div class="region-view">
    <!-- Region Grid -->
    <div class="all-regions-section">
      <h2>All Regions</h2>
      <div class="all-regions-grid">
        <router-link
          v-for="r in allRegions"
          :key="r.id"
          :to="`/regions/${r.id}`"
          class="region-card"
          :class="{ unexplored: !isRegionExplored(r.id) }"
          :title="r.name"
        >
          <span class="region-flag">{{ r.flag_emoji || '🌍' }}</span>
          <span class="region-name">{{ r.name }}</span>
        </router-link>
      </div>
    </div>

    <div class="region-header" v-if="region">
      <div class="region-title">
        <span class="region-flag">{{ region.flag_emoji || '🌍' }}</span>
        <h1>{{ region.name || 'Unexplored Region' }}</h1>
      </div>
      <p class="region-description">{{ region.description || 'Start exploring to unlock this region\'s cultural secrets!' }}</p>
    </div>

    <div class="region-content">
      <div class="subjects-section">
        <h2>Cultural Topics</h2>
        <div v-if="subjects.length" class="subjects-grid">
          <div v-for="subject in subjects" :key="subject.id" class="subject-card">
            <h3>{{ subject.name }}</h3>
            <p>{{ subject.description }}</p>
            <div class="cultural-context" v-if="subject.cultural_context">
              <p>{{ subject.cultural_context }}</p>
            </div>
            <div class="subject-actions">
              <button @click="viewChapters(subject.id)" class="btn-explore">
                Explore Topics
              </button>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">No topics available yet. Start exploring!</div>
      </div>

      <div class="progress-section" v-if="userProgress">
        <h2>Your Progress in {{ region.name }}</h2>
        <div class="progress-stats">
          <div class="stat-card">
            <div class="stat-value">{{ userProgress.completedQuizzes }}</div>
            <div class="stat-label">Quizzes Completed</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ userProgress.averageScore }}%</div>
            <div class="stat-label">Average Score</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ userProgress.culturalPoints }}</div>
            <div class="stat-label">Cultural Points</div>
          </div>
        </div>
      </div>

      <!-- Badges Section -->
      <div class="badges-section">
        <h2>Badges</h2>
        <div class="badges-grid">
          <div
            v-for="badge in allBadges"
            :key="badge.id"
            class="badge-card"
            :class="{ earned: userBadges.some(b => b.id === badge.id) }"
            :title="badge.name + (userBadges.some(b => b.id === badge.id) ? ' (Earned)' : ' (Locked)')"
          >
            <div class="badge-icon">{{ badge.icon || '🏆' }}</div>
            <div class="badge-name">{{ badge.name }}</div>
            <div class="badge-desc">{{ badge.description }}</div>
            <div v-if="!userBadges.some(b => b.id === badge.id)" class="badge-req">
              <span>Requirement: {{ badge.requirement || 'Earn more points!' }}</span>
            </div>
          </div>
        </div>
        <div v-if="!userBadges.length" class="empty-state">No badges earned yet. Keep exploring to unlock badges!</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegionView',
  data() {
    return {
      region: null,
      subjects: [],
      userProgress: null,
      userBadges: [],
      allRegions: [],
      allBadges: []
    }
  },
  async created() {
    await this.fetchAllRegions()
    await this.fetchRegion()
    await this.fetchSubjects()
    await this.fetchUserProgress()
    await this.fetchUserBadges()
    await this.fetchAllBadges()
  },
  methods: {
    async fetchAllRegions() {
      try {
        const response = await fetch('/api/regions', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.allRegions = await response.json()
      } catch (error) {
        this.allRegions = []
      }
    },
    async fetchAllBadges() {
      try {
        const response = await fetch('/api/badges', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.allBadges = await response.json()
      } catch (error) {
        this.allBadges = []
      }
    },
    async fetchRegion() {
      try {
        const response = await fetch(`/api/regions/${this.$route.params.regionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.region = await response.json()
      } catch (error) {
        this.region = { name: '', flag_emoji: '', description: '' }
      }
    },
    async fetchSubjects() {
      try {
        const response = await fetch(`/api/subjects/by-region/${this.$route.params.regionId}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.subjects = await response.json()
      } catch (error) {
        this.subjects = []
      }
    },
    async fetchUserProgress() {
      try {
        const response = await fetch(`/api/regions/${this.$route.params.regionId}/progress`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.userProgress = await response.json()
      } catch (error) {
        this.userProgress = {
          completedQuizzes: 0,
          averageScore: 0,
          culturalPoints: 0
        }
      }
    },
    async fetchUserBadges() {
      try {
        const response = await fetch('/api/user/badges', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.userBadges = await response.json()
      } catch (error) {
        this.userBadges = []
      }
    },
    viewChapters(subjectId) {
      // Find the subject by id
      const subject = this.subjects.find(s => s.id === subjectId);
      if (subject) {
        this.$router.push({
          path: '/home',
          query: { subject: subject.name }
        });
      } else {
        this.$router.push('/home');
      }
    },
    isRegionExplored(regionId) {
      return regionId == this.region?.id || this.userProgress?.culturalPoints > 0 // fallback logic
    }
  }
}
</script>

<style scoped>
.region-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.all-regions-section {
  margin-bottom: 2.5rem;
}
.all-regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1.2rem;
  margin-top: 1rem;
}
.region-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 1.2rem 0.5rem;
  text-align: center;
  color: #2c3e50;
  font-weight: 500;
  font-size: 1.1rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  transition: transform 0.18s, box-shadow 0.18s, background 0.18s;
  cursor: pointer;
  border: 2px solid transparent;
}
.region-card:hover {
  background: #e6f7c7;
  transform: translateY(-4px) scale(1.04);
  box-shadow: 0 4px 12px rgba(76,175,80,0.10);
  border-color: #b2e59e;
}
.region-card.unexplored {
  opacity: 0.5;
  filter: grayscale(0.7);
  cursor: pointer;
}
.region-flag {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.3rem;
}
.region-name {
  font-size: 1rem;
  font-family: var(--font-heading);
}

.region-header {
  text-align: center;
  margin-bottom: 3rem;
}

.region-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.region-description {
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
  font-family: var(--font-content);
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.subject-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}
.subject-card:hover {
  transform: translateY(-5px) scale(1.03);
  box-shadow: 0 4px 12px rgba(76,175,80,0.10);
}
.subject-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-family: var(--font-heading);
}
.cultural-context {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.9rem;
  color: #666;
  font-family: var(--font-content);
}
.subject-actions {
  margin-top: 1.5rem;
}
.btn-explore {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-explore:hover {
  background: #388E3C;
}
.empty-state {
  color: #aaa;
  text-align: center;
  margin: 2rem 0;
  font-size: 1.1rem;
}
.progress-section {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 2px solid #eee;
}
.progress-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}
.stat-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}
.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-family: var(--font-heading);
}
.stat-label {
  color: #666;
  font-size: 0.9rem;
  font-family: var(--font-content);
}
.badges-section {
  margin-top: 3rem;
}
.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.2rem;
  margin-top: 1.2rem;
}
.badge-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 1.2rem;
  text-align: center;
  color: #2c3e50;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  transition: transform 0.18s, box-shadow 0.18s, background 0.18s;
  opacity: 0.6;
  filter: grayscale(0.5);
}
.badge-card.earned {
  opacity: 1;
  filter: none;
  background: #e6f7c7;
  box-shadow: 0 4px 12px rgba(76,175,80,0.10);
}
.badge-card:hover {
  transform: translateY(-4px) scale(1.04);
  box-shadow: 0 4px 12px rgba(76,175,80,0.13);
}
.badge-icon {
  font-size: 2.2rem;
  margin-bottom: 0.4rem;
}
.badge-name {
  font-weight: 600;
  margin-bottom: 0.2rem;
  font-family: var(--font-heading);
}
.badge-desc {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 0.3rem;
  font-family: var(--font-content);
}
.badge-req {
  font-size: 0.9rem;
  color: #b77;
  font-family: var(--font-content);
}
</style> 