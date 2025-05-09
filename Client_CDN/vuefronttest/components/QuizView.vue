<template>
  <div class="quiz-view">
    <div class="quiz-header">
      <h1>{{ quiz.title }}</h1>
      <div class="quiz-info">
        <span>Duration: {{ formatDuration(quiz.time_duration) }}</span>
        <span>Questions: {{ quiz.questions.length }}</span>
      </div>
    </div>

    <div class="quiz-content">
      <div v-for="(question, index) in quiz.questions" :key="question.id" class="question-card">
        <div class="question-header">
          <h3>Question {{ index + 1 }}</h3>
          <cultural-context :question-id="question.id" />
        </div>
        
        <p class="question-text">{{ question.question_statement }}</p>
        
        <div class="options-grid">
          <div v-for="(option, optIndex) in question.options" 
               :key="optIndex"
               class="option-card"
               :class="{ 
                 'selected': selectedAnswers[question.id] === optIndex + 1,
                 'correct': showResults && optIndex + 1 === question.correct_option,
                 'incorrect': showResults && selectedAnswers[question.id] === optIndex + 1 && optIndex + 1 !== question.correct_option
               }"
               @click="selectAnswer(question.id, optIndex + 1)">
            {{ option }}
          </div>
        </div>
      </div>
    </div>

    <div class="quiz-actions">
      <button @click="submitQuiz" 
              :disabled="!canSubmit || isSubmitting"
              class="submit-btn">
        {{ isSubmitting ? 'Submitting...' : 'Submit Quiz' }}
      </button>
    </div>

    <div v-if="showResults" class="quiz-results">
      <h2>Quiz Results</h2>
      <div class="results-stats">
        <div class="stat">
          <span class="label">Score:</span>
          <span class="value">{{ score }}%</span>
        </div>
        <div class="stat">
          <span class="label">Cultural Points Earned:</span>
          <span class="value">{{ culturalPointsEarned }}</span>
        </div>
      </div>
      <button @click="viewDetailedReport" class="view-report-btn">
        View Detailed Report
      </button>
    </div>
  </div>
</template>

<script>
import CulturalContext from './CulturalContext.vue'

export default {
  name: 'QuizView',
  components: {
    CulturalContext
  },
  data() {
    return {
      quiz: {
        title: '',
        time_duration: '',
        questions: []
      },
      selectedAnswers: {},
      showResults: false,
      score: 0,
      culturalPointsEarned: 0,
      isSubmitting: false
    }
  },
  computed: {
    canSubmit() {
      return Object.keys(this.selectedAnswers).length === this.quiz.questions.length
    }
  },
  async created() {
    await this.fetchQuiz()
  },
  methods: {
    async fetchQuiz() {
      try {
        const response = await fetch(`/api/quizzes/${this.$route.params.quizid}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        })
        this.quiz = await response.json()
      } catch (error) {
        console.error('Error fetching quiz:', error)
      }
    },
    selectAnswer(questionId, optionIndex) {
      if (!this.showResults) {
        this.$set(this.selectedAnswers, questionId, optionIndex)
      }
    },
    formatDuration(duration) {
      // Convert duration string to minutes
      const minutes = parseInt(duration.split(':')[0])
      return `${minutes} minutes`
    },
    async submitQuiz() {
      if (!this.canSubmit || this.isSubmitting) return

      this.isSubmitting = true
      try {
        const response = await fetch(`/api/quizzes/${this.$route.params.quizid}/submit`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            answers: this.selectedAnswers
          })
        })

        const result = await response.json()
        this.score = result.score
        this.culturalPointsEarned = result.cultural_points_earned
        this.showResults = true
      } catch (error) {
        console.error('Error submitting quiz:', error)
      } finally {
        this.isSubmitting = false
      }
    },
    viewDetailedReport() {
      this.$router.push(`/scores/${this.scoreId}`)
    }
  }
}
</script>

<style scoped>
.quiz-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.quiz-header {
  text-align: center;
  margin-bottom: 2rem;
}

.quiz-info {
  display: flex;
  justify-content: center;
  gap: 2rem;
  color: #666;
  margin-top: 1rem;
}

.question-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.question-text {
  font-size: 1.1rem;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.options-grid {
  display: grid;
  gap: 1rem;
}

.option-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-card:hover {
  background: #e9ecef;
}

.option-card.selected {
  background: #e3f2fd;
  border: 2px solid #2196f3;
}

.option-card.correct {
  background: #e8f5e9;
  border: 2px solid #4caf50;
}

.option-card.incorrect {
  background: #ffebee;
  border: 2px solid #f44336;
}

.quiz-actions {
  text-align: center;
  margin-top: 2rem;
}

.submit-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 25px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #388e3c;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.quiz-results {
  margin-top: 3rem;
  text-align: center;
}

.results-stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin: 2rem 0;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat .label {
  color: #666;
  margin-bottom: 0.5rem;
}

.stat .value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.view-report-btn {
  background: #2196f3;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.2s;
}

.view-report-btn:hover {
  background: #1976d2;
}
</style> 