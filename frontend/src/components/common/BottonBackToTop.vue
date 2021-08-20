<template>
    <v-row @click="scrollTop">
    <font-awesome-icon class="Page-Btn-Icon Page-Btn" :icon="['fas', 'chevron-up']"></font-awesome-icon>
    </v-row>
</template>

<script>
export default {
    name:"ButtonBackToTop",
    methods: {
        scrollTop: function(){
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
        }
    }
}
</script>

<style lang="scss" scoped>
.Page-Btn{
  position: fixed;
  right: 30px;
  bottom: 40px;
  width: 40px;
  height: 40px;
  line-height: 32px;
  text-align: center;
  border-radius: 50%;
  background: #5bc8ac;
}
.Page-Btn-Icon{
  color: #fff;
  font-size: 16px;
}
</style>
