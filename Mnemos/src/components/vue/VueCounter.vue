<template>
  <div class="vue-counter-component p-6 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
    <h3 class="text-xl font-semibold mb-4 text-green-800 dark:text-green-200">
      Vue.js Counter Component
    </h3>
    
    <div class="flex items-center space-x-4">
      <button 
        @click="decrement"
        class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md transition-colors duration-200"
        :disabled="count <= 0"
      >
        -
      </button>
      
      <div class="text-2xl font-bold text-green-700 dark:text-green-300 min-w-[3rem] text-center">
        {{ count }}
      </div>
      
      <button 
        @click="increment"
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md transition-colors duration-200"
      >
        +
      </button>
    </div>
    
    <div class="mt-4">
      <button 
        @click="reset"
        class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-md transition-colors duration-200"
      >
        Reset
      </button>
    </div>
    
    <p class="mt-4 text-sm text-green-600 dark:text-green-400">
      This is a Vue.js component that will be integrated with the React application.
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const count = ref(0)

const increment = () => {
  count.value++
}

const decrement = () => {
  if (count.value > 0) {
    count.value--
  }
}

const reset = () => {
  count.value = 0
}
</script>

<style scoped>
.vue-counter-component {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button:disabled:hover {
  background-color: inherit;
}
</style>