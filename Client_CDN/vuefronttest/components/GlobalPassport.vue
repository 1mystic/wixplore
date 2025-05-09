<template>
  <div class="global-passport">
    <div class="passport-header">
      <h2>Global Knowledge Passport</h2>
      <div class="total-points">
        <span class="points-label">Cultural Points:</span>
        <span class="points-value">{{ passport.total_cultural_points }}</span>
      </div>
    </div>

    <div class="passport-content">
      <div class="regions-section">
        <h3>Regions Explored</h3>
        <div class="regions-grid">
          <div v-for="(date, regionId) in passport.regions_explored" :key="regionId" class="region-card">
            <div class="region-flag">{{ getRegionFlag(regionId) }}</div>
            <div class="region-name">{{ getRegionName(regionId) }}</div>
            <div class="exploration-date">Explored: {{ formatDate(date) }}</div>
          </div>
        </div>
      </div>

      <div class="badges-section">
        <h3>Badges Earned</h3>
        <div class="badges-grid">
          <div v-for="badge in passport.badges_earned" :key="badge" class="badge-card">
            <div class="badge-icon">🏆</div>
            <div class="badge-name">{{ badge }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GlobalPassport',
  data() {
    return {
      passport: {
        regions_explored: {},
        total_cultural_points: 0,
        badges_earned: []
      },
      regions: []
    }
  },
  async created() {
    await this.fetchPassport()
    await this.fetchRegions()
  },
  methods: {
    async fetchPassport() {
      try {
        const response = await fetch('/api/user/passport', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        const data = await response.json()
        this.passport = data
      } catch (error) {
        console.error('Error fetching passport:', error)
      }
    },
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
    getRegionFlag(regionId) {
      const region = this.regions.find(r => r.id === parseInt(regionId))
      return region ? region.flag_emoji : '🌍'
    },
    getRegionName(regionId) {
      const region = this.regions.find(r => r.id === parseInt(regionId))
      return region ? region.name : 'Unknown Region'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.global-passport {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.passport-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.total-points {
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.points-label {
  color: #666;
  margin-right: 0.5rem;
}

.points-value {
  font-weight: bold;
  color: #2c3e50;
}

.regions-grid, .badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.region-card, .badge-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.2s;
}

.region-card:hover, .badge-card:hover {
  transform: translateY(-5px);
}

.region-flag, .badge-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.region-name, .badge-name {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.exploration-date {
  font-size: 0.9rem;
  color: #666;
}

.badges-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #eee;
}

h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}
</style> 