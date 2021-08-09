<template>
  <v-app id="app">
    <Navbar />
    <v-main class="main__conteiner">
      <!-- <AdSense></AdSense> -->
      <!-- <tipping></tipping> -->
      <router-view></router-view>
    </v-main>
    <Footer />
  </v-app>
</template>

<script>
import Navbar from './components/common/Navbar'
import Footer from './components/common/Footer'
// import AdSense from './components/common/AdSense'
// import Tipping from './components/common/Tipping.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
    // 'tipping': Tipping
  },
  data: () => ({
    //
  })
}
</script>

<style lang="scss" scoped>
.main__conteiner {
  margin: auto;
  padding: 20px !important;
  font-size: 0.75rem;
}

.main__conteiner h1 {
  font-size: 1.25rem;
}

.main__conteiner h2 {
  font-size: 1rem;
  margin: 2px;
}

.main__conteiner h3 {
  font-size: 13px;
}
</style>
