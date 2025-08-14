<template>
  <div>
    <button @click="runWorkflow" class="btn btn-primary">Run Agents</button>
    <pre v-if="result">{{ result }}</pre>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { runAgents } from '../../services/agentService'
const result = ref(null)
const runWorkflow = async () => {
  result.value = await runAgents({ dataset: "example" })
}
</script>
