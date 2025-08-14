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
        <h3>All Regions</h3>
        <div class="regions-grid">
          <router-link
            v-for="region in regions"
            :key="region.id"
            :to="`/regions/${region.id}`"
            class="region-card"
            :class="{ explored: isRegionExplored(region.id), unexplored: !isRegionExplored(region.id) }"
            :title="region.name + (isRegionExplored(region.id) ? ' (Explored)' : ' (Unexplored)')"
          >
            <div class="region-flag">{{ region.flag_emoji || '🌍' }}</div>
            <div class="region-name">{{ region.name }}</div>
            <div class="exploration-date" v-if="isRegionExplored(region.id)">Explored</div>
            <div class="exploration-date" v-else>Not Explored</div>
          </router-link>
        </div>
        <div v-if="regions.length === 0" class="empty-state">No regions available. Please contact admin.</div>
      </div>

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
      regions: [],
      allBadges: [],
      userBadges: []
    }
  },
  async created() {
    await this.fetchPassport()
    await this.fetchRegions()
    await this.fetchAllBadges()
    await this.fetchUserBadges()
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
    isRegionExplored(regionId) {
      return this.passport.regions_explored && this.passport.regions_explored[String(regionId)] !== undefined
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

.regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
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
  opacity: 1;
  filter: none;
  text-decoration: none;
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
.region-card.explored {
  background: #E8F5E9;
  border: 2px solid #4CAF50;
  opacity: 1;
  filter: none;
}
.region-flag {
  font-size: 2rem;
  display: block;
  margin-bottom: 0.3rem;
}
.region-name {
  font-size: 1rem;
}
.exploration-date {
  font-size: 0.9rem;
  color: #666;
}
.badges-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 2px solid #eee;
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
h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}
</style> 