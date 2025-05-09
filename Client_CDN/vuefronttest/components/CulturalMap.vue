<template>
  <div class="cultural-map">
    <div class="map-header">
      <h2>Your Cultural Knowledge Map</h2>
      <p>Explore your journey through global cultures and knowledge</p>
    </div>

    <div class="map-container">
      <div class="world-map">
        <div v-for="region in regions" 
             :key="region.id" 
             class="region-area"
             :class="{ 'explored': isRegionExplored(region.id) }"
             @click="navigateToRegion(region.id)">
          <div class="region-info">
            <span class="region-flag">{{ region.flag_emoji }}</span>
            <span class="region-name">{{ region.name }}</span>
            <div class="exploration-status" v-if="isRegionExplored(region.id)">
              <span class="status-dot"></span>
              Explored
            </div>
          </div>
        </div>
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
      }
    }
  },
  computed: {
    totalRegionsExplored() {
      return Object.keys(this.passport.regions_explored).length
    },
    totalSubjects() {
      // This would be calculated based on completed subjects
      return 12
    },
    totalBadges() {
      return this.passport.badges_earned.length
    },
    totalPoints() {
      return this.passport.total_cultural_points
    }
  },
  async created() {
    await this.fetchRegions()
    await this.fetchPassport()
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
    isRegionExplored(regionId) {
      return this.passport.regions_explored[regionId] !== undefined
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
}

.region-area:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.region-area.explored {
  background: #E8F5E9;
  border: 2px solid #4CAF50;
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
</style> 