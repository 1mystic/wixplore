<template>
  <router-view :key="$route.fullPath"></router-view>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Mitr:wght@200;300;400;500;600;700&family=Rubik:wght@300;400;500;600;700&display=swap');

:root {
  --font-heading: 'Mitr', sans-serif;
  --font-content: 'Rubik', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  color: rgba(58, 27, 35, 0.822);
  font-weight: 600;
}

body {
  font-family: var(--font-content);
  font-weight: 400;
}

/* Apply Mitr to all headings */
.section-title,
.quiz-title,
.journey-title,
.region-title h1,
.category-card span,
.badge-name {
  font-family: var(--font-heading);
}

/* Apply Rubik to all content */
.quiz-subtitle,
.region-description,
.journey-subtitle,
.badge-desc,
.quiz-card-img-title,
.score_card_id,
.filter_opt .form-check-label,
.search_bar input.form-control {
  font-family: var(--font-content);
}
</style> 