<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
/* 可以在这里添加全局样式 */

html, body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  height: 100%;
  line-height: 1.6;
  color: #333;
}

#app {
  height: 100%;
}
</style>
