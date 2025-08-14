<template>
    <div v-if="isLoading" class="loading-container card">
        <p>Loading Quiz Results...</p>
        </div>

    <div v-else-if="error" class="error-container card error-card">
        <p>Error loading results: {{ error }}</p>
    </div>
     
    <div v-else-if="reportData" class="results-container"> <div class="card">
           
            <h1 class="score_head">Quiz Summary : <span v-if="reportData.user">{{ reportData.user }}</span></h1>
            
            <div class="score_enc">
            <router-link to="/home" class="back-button">Back</router-link>
                <h5>Quiz: {{ reportData.quiz_title }}</h5>
                <p>Score: {{ reportData.score ? reportData.score.toFixed(2) : 'N/A' }}%</p>
                <button @click="savepage" class="s_save_btn">Save</button>
            </div>
        </div>

        <div v-if="reportData.ai_report" class="card ai-report-card">
            <h2 class="report-title">AI Analysis Report</h2>
            <div v-if="reportData.ai_report.summary">
                <h3>Summary</h3>
                <p class="ai_overview">{{ reportData.ai_report.summary }}</p>
            </div>
            <div v-if="reportData.ai_report.strengths && reportData.ai_report.strengths.length > 0">
                <h3>Strengths</h3>
                <ul>
                    <li v-for="(strength, index) in reportData.ai_report.strengths" :key="'strength-' + index">{{ strength }}</li>
                </ul>
            </div>
             <div v-if="reportData.ai_report.weaknesses && reportData.ai_report.weaknesses.length > 0">
                <h3>Areas for Improvement</h3>
                <ul>
                    <li v-for="(weakness, index) in reportData.ai_report.weaknesses" :key="'weakness-' + index">{{ weakness }}</li>
                </ul>
            </div>
             <div v-if="reportData.ai_report.suggestions && reportData.ai_report.suggestions.length > 0">
                <h3>Suggestions</h3>
                <ul>
                    <li v-for="(suggestion, index) in reportData.ai_report.suggestions" :key="'suggestion-' + index">{{ suggestion }}</li>
                </ul>
            </div>
             <div v-if="!reportData.ai_report.summary && !reportData.ai_report.strengths?.length && !reportData.ai_report.weaknesses?.length && !reportData.ai_report.suggestions?.length">
                 <p>AI analysis data is empty or unavailable for this attempt.</p>
             </div>
        </div>

        <div class="quiz-history card"> <h2 class="report-title">Question Breakdown</h2>
            <table class="score-table" v-if="reportData.questions && reportData.questions.length > 0">
                <thead>
                    <tr>
                        <th>Question</th>
                        <th>Your Answer</th>
                        <th>Correct Answer</th>
                        <th>Outcome</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(question, index) in reportData.questions" :key="'q-' + index">
                        <td>Q{{ index + 1 }}: {{ question.question }}</td>
                        <td>{{ question.selected_option !== null ? question.selected_option : 'Not Answered' }}</td>
                        <td>{{ question.correct_option }}</td>
                        <td :class="{'correct': question.selected_option === question.correct_option, 'incorrect': question.selected_option !== question.correct_option && question.selected_option !== null}">
                            {{ getOutcomeText(question) }}
                        </td>
                    </tr>
                </tbody>
            </table>
            <p v-else>No question history available.</p>
        </div>

    </div>

    <div v-else class="loading-container card"> <p>Could not load report data.</p>
    </div>
    `,
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: 'UserScore',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    // Convert data() to refs
            
            reportData: ref(null), // Single object to hold all fetched data
            isLoading: ref(true), // Unified loading state
            error: ref(null), // Unified error state
        };
    
    
    // Convert methods to functions
            fetchFullReport() {
            const scoreId = this.$route.params.Id; // Get scoreId from route
            if (!scoreId) {
                this.error = 'Error: Score ID not found in route parameters.';
                this.isLoading = false;
                console.error(this.error);
                return;
            }

            this.isLoading = true;
            this.error = null; // Reset error

            fetch(`http://127.0.0.1:5000/api/scores/${scoreId}/full_report`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                     // Try to get error message from response body
                     return response.json().then(errData => {
                         throw new Error(errData.message || `HTTP error! status: ${response.status}`);
                     }).catch(() => {
                         // Fallback if response body isn't JSON or doesn't have message
                         throw new Error(`HTTP error! status: ${response.status}`);
                     });
                }
                return response.json();
            })
            .then(data => {
                this.reportData = data; // Store the entire combined response
            })
            .catch(error => {
                console.error('Error fetching full report:', error);
                this.error = error.message; // Display error message
                this.reportData = null; // Ensure no stale data is shown
            })
            .finally(() => {
                this.isLoading = false;
            });
        

        getOutcomeText(question) {
            if (question.selected_option === null) {
                return 'Not Answered';
            }
            return question.selected_option === question.correct_option ? 'Correct' : 'Incorrect';
        

        savepage() {
            // Consider adding specific classes for printing to hide unnecessary elements
            window.print();
        }
    
    
    // Convert created() to onMounted
    
    
    // Convert computed to computed properties
    
    
    return {
      // Return all reactive variables and methods
      
reportData
isLoading
error
};,
      // Return all methods
      fetchFullReport() {
const scoreId = this.$route.params.Id; // Get scoreId from route
if (!scoreId) {
this.error = 'Error: Score ID not found in route parameters.';
this.isLoading = false;
console.error(this.error);
return;
}

this.isLoading = true;
this.error = null; // Reset error

fetch(`http://127.0.0.1:5000/api/scores/${scoreId}/full_report`, {
headers: {
'Authorization': `Bearer ${localStorage.getItem('token')}`,
'Content-Type': 'application/json'
}
})
.then(response => {
if (!response.ok) {
// Try to get error message from response body
return response.json().then(errData => {
throw new Error(errData.message || `HTTP error! status: ${response.status}`);
}).catch(() => {
// Fallback if response body isn't JSON or doesn't have message
throw new Error(`HTTP error! status: ${response.status}`);
});
}
return response.json();
})
.then(data => {
this.reportData = data; // Store the entire combined response
})
.catch(error => {
console.error('Error fetching full report:', error);
this.error = error.message; // Display error message
this.reportData = null; // Ensure no stale data is shown
})
.finally(() => {
this.isLoading = false;
});


getOutcomeText(question) {
if (question.selected_option === null) {
return 'Not Answered';
}
return question.selected_option === question.correct_option ? 'Correct' : 'Incorrect';


savepage() {
// Consider adding specific classes for printing to hide unnecessary elements
window.print();
},
      // Return all computed properties
      
    }
  }
}
</script>

<style scoped>

</style>
