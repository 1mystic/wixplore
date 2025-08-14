#!/bin/bash

# Create necessary directories if they don't exist
mkdir -p src/views/admin
mkdir -p src/components
mkdir -p src/assets

# Copy assets
cp -r ../vuefronttest/assets/* src/assets/

# Convert .js files to .vue files
for file in ../vuefronttest/components/*.js; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .js)
        # Convert to PascalCase for component names
        component_name=$(echo "$filename" | sed -r 's/(^|_)([a-z])/\U\2/g')
        
        # Create Vue component structure
        echo "<template>
$(grep -A 1000 'template:' "$file" | grep -B 1000 'data()' | sed '1d' | sed '$d')
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: '$component_name',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    // Convert data() to refs
    $(grep -A 1000 'data()' "$file" | grep -B 1000 'methods:' | sed '1d' | sed '$d' | sed 's/return {//' | sed 's/},//' | sed 's/: /: ref(/' | sed 's/,/),/g' | sed 's/}),/})/g')
    
    // Convert methods to functions
    $(grep -A 1000 'methods:' "$file" | grep -B 1000 'created()' | sed '1d' | sed '$d' | sed 's/methods: {//' | sed 's/},//' | sed 's/: function/ = function/g')
    
    // Convert created() to onMounted
    $(grep -A 1000 'created()' "$file" | grep -B 1000 'computed:' | sed '1d' | sed '$d' | sed 's/created()/onMounted(() => {/' | sed 's/},/})/g')
    
    // Convert computed to computed properties
    $(grep -A 1000 'computed:' "$file" | grep -B 1000 'watch:' | sed '1d' | sed '$d' | sed 's/computed: {//' | sed 's/},//' | sed 's/: function/ = computed(() => {/g' | sed 's/},/})/g')
    
    return {
      // Return all reactive variables and methods
      $(grep -A 1000 'data()' "$file" | grep -B 1000 'methods:' | sed '1d' | sed '$d' | sed 's/return {//' | sed 's/},//' | sed 's/: .*//' | sed 's/^[ \t]*//'),
      // Return all methods
      $(grep -A 1000 'methods:' "$file" | grep -B 1000 'created()' | sed '1d' | sed '$d' | sed 's/methods: {//' | sed 's/},//' | sed 's/: function.*//' | sed 's/^[ \t]*//'),
      // Return all computed properties
      $(grep -A 1000 'computed:' "$file" | grep -B 1000 'watch:' | sed '1d' | sed '$d' | sed 's/computed: {//' | sed 's/},//' | sed 's/: function.*//' | sed 's/^[ \t]*//')
    }
  }
}
</script>

<style scoped>
$(grep -A 1000 'addStyles' "$file" | grep -B 1000 '});' | sed '1d' | sed '$d' | sed 's/addStyles(//' | sed 's/});/}/')
</style>" > "src/views/$component_name.vue"
    fi
done

# Copy existing .vue files
cp ../vuefronttest/components/*.vue src/views/

# Convert admin components
for file in ../vuefronttest/components/admin_data/*.js; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .js)
        component_name=$(echo "$filename" | sed -r 's/(^|_)([a-z])/\U\2/g')
        
        # Create Vue component structure for admin components
        echo "<template>
$(grep -A 1000 'template:' "$file" | grep -B 1000 'data()' | sed '1d' | sed '$d')
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: '$component_name',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    // Convert data() to refs
    $(grep -A 1000 'data()' "$file" | grep -B 1000 'methods:' | sed '1d' | sed '$d' | sed 's/return {//' | sed 's/},//' | sed 's/: /: ref(/' | sed 's/,/),/g' | sed 's/}),/})/g')
    
    // Convert methods to functions
    $(grep -A 1000 'methods:' "$file" | grep -B 1000 'created()' | sed '1d' | sed '$d' | sed 's/methods: {//' | sed 's/},//' | sed 's/: function/ = function/g')
    
    // Convert created() to onMounted
    $(grep -A 1000 'created()' "$file" | grep -B 1000 'computed:' | sed '1d' | sed '$d' | sed 's/created()/onMounted(() => {/' | sed 's/},/})/g')
    
    // Convert computed to computed properties
    $(grep -A 1000 'computed:' "$file" | grep -B 1000 'watch:' | sed '1d' | sed '$d' | sed 's/computed: {//' | sed 's/},//' | sed 's/: function/ = computed(() => {/g' | sed 's/},/})/g')
    
    return {
      // Return all reactive variables and methods
      $(grep -A 1000 'data()' "$file" | grep -B 1000 'methods:' | sed '1d' | sed '$d' | sed 's/return {//' | sed 's/},//' | sed 's/: .*//' | sed 's/^[ \t]*//'),
      // Return all methods
      $(grep -A 1000 'methods:' "$file" | grep -B 1000 'created()' | sed '1d' | sed '$d' | sed 's/methods: {//' | sed 's/},//' | sed 's/: function.*//' | sed 's/^[ \t]*//'),
      // Return all computed properties
      $(grep -A 1000 'computed:' "$file" | grep -B 1000 'watch:' | sed '1d' | sed '$d' | sed 's/computed: {//' | sed 's/},//' | sed 's/: function.*//' | sed 's/^[ \t]*//')
    }
  }
}
</script>

<style scoped>
$(grep -A 1000 'addStyles' "$file" | grep -B 1000 '});' | sed '1d' | sed '$d' | sed 's/addStyles(//' | sed 's/});/}/')
</style>" > "src/views/admin/$component_name.vue"
    fi
done

# Convert user components
for file in ../vuefronttest/components/Users/*.js; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .js)
        component_name=$(echo "$filename" | sed -r 's/(^|_)([a-z])/\U\2/g')
        
        # Create Vue component structure for user components
        echo "<template>
$(grep -A 1000 'template:' "$file" | grep -B 1000 'data()' | sed '1d' | sed '$d')
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default {
  name: '$component_name',
  setup() {
    const router = useRouter()
    const store = useStore()
    
    // Convert data() to refs
    $(grep -A 1000 'data()' "$file" | grep -B 1000 'methods:' | sed '1d' | sed '$d' | sed 's/return {//' | sed 's/},//' | sed 's/: /: ref(/' | sed 's/,/),/g' | sed 's/}),/})/g')
    
    // Convert methods to functions
    $(grep -A 1000 'methods:' "$file" | grep -B 1000 'created()' | sed '1d' | sed '$d' | sed 's/methods: {//' | sed 's/},//' | sed 's/: function/ = function/g')
    
    // Convert created() to onMounted
    $(grep -A 1000 'created()' "$file" | grep -B 1000 'computed:' | sed '1d' | sed '$d' | sed 's/created()/onMounted(() => {/' | sed 's/},/})/g')
    
    // Convert computed to computed properties
    $(grep -A 1000 'computed:' "$file" | grep -B 1000 'watch:' | sed '1d' | sed '$d' | sed 's/computed: {//' | sed 's/},//' | sed 's/: function/ = computed(() => {/g' | sed 's/},/})/g')
    
    return {
      // Return all reactive variables and methods
      $(grep -A 1000 'data()' "$file" | grep -B 1000 'methods:' | sed '1d' | sed '$d' | sed 's/return {//' | sed 's/},//' | sed 's/: .*//' | sed 's/^[ \t]*//'),
      // Return all methods
      $(grep -A 1000 'methods:' "$file" | grep -B 1000 'created()' | sed '1d' | sed '$d' | sed 's/methods: {//' | sed 's/},//' | sed 's/: function.*//' | sed 's/^[ \t]*//'),
      // Return all computed properties
      $(grep -A 1000 'computed:' "$file" | grep -B 1000 'watch:' | sed '1d' | sed '$d' | sed 's/computed: {//' | sed 's/},//' | sed 's/: function.*//' | sed 's/^[ \t]*//')
    }
  }
}
</script>

<style scoped>
$(grep -A 1000 'addStyles' "$file" | grep -B 1000 '});' | sed '1d' | sed '$d' | sed 's/addStyles(//' | sed 's/});/}/')
</style>" > "src/views/$component_name.vue"
    fi
done

echo "Conversion complete! Please review the converted files in src/views/ and src/views/admin/" 