<script setup>
const name = "Dawid Garncarek"
const subject = "Programowanie aplikacji webowych"
</script>

<template>
  <div id="app">
    <h1>Witaj, {{ name }}!</h1>
    <p>Temat zajęć: {{ subject }}</p>
  </div>
</template>

<style>
h1 {
  color: #42b983;
}
</style>
