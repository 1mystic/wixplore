<template>
  <div class="cultural-map">
    <div class="map-header">
      <h2>Your Cultural Knowledge Map</h2>
      <p>Explore your journey through global cultures and knowledge</p>
    </div>

    <div class="map-container">
      <div class="world-map">
        <router-link
          v-for="region in regions"
          :key="region.id"
          :to="`/regions/${region.id}`"
          class="region-area"
          :class="{ explored: isRegionExplored(region.id), unexplored: !isRegionExplored(region.id) }"
          :title="region.name + (isRegionExplored(region.id) ? ' (Explored)' : ' (Unexplored)')"
        >
          <div class="region-info">
            <span class="region-flag">{{ region.flag_emoji || '🌍' }}</span>
            <span class="region-name">{{ region.name }}</span>
            <div class="exploration-status" v-if="isRegionExplored(region.id)">
              <span class="status-dot"></span>
              Explored
            </div>
            <div class="exploration-status" v-else>
              <span class="status-dot unexplored-dot"></span>
              Not Explored
            </div>
          </div>
        </router-link>
      </div>

      <div class="map-legend">
        <div class="legend-item">
          <div class="legend-color explored"></div>
          <span>Regions Explored</span>
        </div>
        <div class="legend-item">
          <div class="legend-color"></div>
          <span>Regions to Discover</span>
        </div>
      </div>
    </div>

    <div v-if="regions.length === 0" class="empty-state">No regions available. Please contact admin.</div>
    <div v-else-if="totalRegionsExplored === 0" class="empty-state">You haven't explored any regions yet. Start your journey by clicking a region!</div>

    <div class="knowledge-stats">
      <h3>Your Global Knowledge Journey</h3>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">🌍</div>
          <div class="stat-value">{{ totalRegionsExplored }}</div>
          <div class="stat-label">Regions Explored</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-value">{{ totalSubjects }}</div>
          <div class="stat-label">Topics Mastered</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏆</div>
          <div class="stat-value">{{ totalBadges }}</div>
          <div class="stat-label">Badges Earned</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-value">{{ totalPoints }}</div>
          <div class="stat-label">Cultural Points</div>
        </div>
      </div>
    </div>

    <!-- Badges Section -->
    <div class="badges-section">
      <h3>All Badges</h3>
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
            <span>Requirement: {{ badge.criteria || 'Earn more points!' }}</span>
          </div>
        </div>
      </div>
      <div v-if="!userBadges.length" class="empty-state">No badges earned yet. Keep exploring to unlock badges!</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CulturalMap',
  data() {
    return {
      regions: [],
      passport: {
        regions_explored: {},
        total_cultural_points: 0,
        badges_earned: []
      },
      allBadges: [],
      userBadges: [],
      userScores: [],
      chapters: [],
      quizzes: []
    }
  },
  computed: {
    totalRegionsExplored() {
      return Object.keys(this.passport.regions_explored).length
    },
    totalSubjects() {
      // Calculate mastered topics/chapters: avg score > 80% in all quizzes in a chapter
      if (!this.userScores.length || !this.chapters.length || !this.quizzes.length) return 0;
      let mastered = 0;
      for (const chapter of this.chapters) {
        const chapterQuizzes = this.quizzes.filter(q => q.chapter_id === chapter.id);
        if (!chapterQuizzes.length) continue;
        const quizIds = chapterQuizzes.map(q => q.id);
        const scores = this.userScores.filter(s => quizIds.includes(s.quiz_id));
        if (!scores.length) continue;
        const avg = scores.reduce((a, b) => a + b.score, 0) / scores.length;
        if (avg >= 80) mastered++;
      }
      return mastered;
    },
    totalBadges() {
      return this.userBadges.length
    },
    totalPoints() {
      return this.passport.total_cultural_points
    }
  },
  async created() {
    await this.fetchRegions()
    await this.fetchPassport()
    await this.fetchAllBadges()
    await this.fetchUserBadges()
    await this.fetchUserScores()
    await this.fetchChapters()
    await this.fetchQuizzes()
  },
  methods: {
    async fetchRegions() {
      try {
        const response = await fetch('/api/regions', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.regions = await response.json()
      } catch (error) {
        console.error('Error fetching regions:', error)
      }
    },
    async fetchPassport() {
      try {
        const response = await fetch('/api/user/passport', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.passport = await response.json()
      } catch (error) {
        console.error('Error fetching passport:', error)
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
        console.error('Error fetching all badges:', error)
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
        console.error('Error fetching user badges:', error)
      }
    },
    async fetchUserScores() {
      try {
        const response = await fetch('/api/users/scores', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.userScores = await response.json()
      } catch (error) {
        this.userScores = [];
      }
    },
    async fetchChapters() {
      try {
        const response = await fetch('/api/chapters', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.chapters = await response.json()
      } catch (error) {
        this.chapters = [];
      }
    },
    async fetchQuizzes() {
      try {
        const response = await fetch('/api/quizzes', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.quizzes = await response.json()
      } catch (error) {
        this.quizzes = [];
      }
    },
    isRegionExplored(regionId) {
      return this.passport.regions_explored && this.passport.regions_explored[String(regionId)] !== undefined
    },
    navigateToRegion(regionId) {
      this.$router.push(`/regions/${regionId}`)
    }
  }
}
</script>

<style scoped>
.cultural-map {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.map-header {
  text-align: center;
  margin-bottom: 3rem;
}

.map-header h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.map-header p {
  color: #666;
}

.map-container {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 3rem;
}

.world-map {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.region-area {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  border: 2px solid transparent;
  opacity: 1;
  filter: none;
}
.region-area:hover {
  transform: translateY(-5px) scale(1.03);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-color: #b2e59e;
  background: #e6f7c7;
}
.region-area.unexplored {
  opacity: 0.5;
  filter: grayscale(0.7);
  cursor: pointer;
}
.region-area.explored {
  background: #E8F5E9;
  border: 2px solid #4CAF50;
  opacity: 1;
  filter: none;
}
.region-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.region-flag {
  font-size: 2rem;
}
.region-name {
  font-weight: 600;
  color: #2c3e50;
}
.exploration-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #4CAF50;
}
.status-dot {
  width: 8px;
  height: 8px;
  background: #4CAF50;
  border-radius: 50%;
}
.status-dot.unexplored-dot {
  background: #aaa;
}
.map-legend {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background: #f8f9fa;
  border: 2px solid #ddd;
}
.legend-color.explored {
  background: #E8F5E9;
  border-color: #4CAF50;
}
.knowledge-stats {
  margin-top: 3rem;
}
.knowledge-stats h3 {
  text-align: center;
  margin-bottom: 2rem;
  color: #2c3e50;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}
.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.stat-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
}
.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}
.stat-label {
  color: #666;
  font-size: 0.9rem;
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
}
.badge-desc {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 0.3rem;
}
.badge-req {
  font-size: 0.9rem;
  color: #b77;
}
.empty-state {
  color: #aaa;
  text-align: center;
  margin: 2rem 0;
  font-size: 1.1rem;
}
</style> 