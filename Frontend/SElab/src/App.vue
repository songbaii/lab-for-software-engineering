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
/* 隐藏浏览器默认密码切换按钮 */
/* 针对所有密码输入框的通用解决方案 */
input[type="password"] {
    /* 隐藏Edge的眼睛图标 */
    &::-ms-reveal {
        display: none;
    }
    
    /* 隐藏Chrome/Safari的自动填充图标 */
    &::-webkit-contacts-auto-fill-button,
    &::-webkit-credentials-auto-fill-button {
        display: none !important;
    }
    
    /* 隐藏Firefox的密码显示按钮（如果需要） */
    &::-moz-text-field-decoration {
        display: none;
    }
}</style>
