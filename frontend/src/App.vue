<template>
  <v-app>
    <!-- <navbar-view></navbar-view> -->
    <v-main cass="main__conteiner">
      <router-view />
    </v-main>
    <footer-view></footer-view>
  </v-app>
</template>

<script>
// import Navbar from './components/common/Navbar'
import Footer from './components/common/Footer'

export default {
  name: "App",
  components: {
    // "navbar-view": Navbar,
    "footer-view": Footer
  },

  data: () => ({
    //
  }),
};
</script>
<style lang="scss">
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
