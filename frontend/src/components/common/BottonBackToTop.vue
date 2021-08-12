<template>
    <div class="Page-Btn" @click="scrollTop">
    <i class="fas fa-chevron-up Page-Btn-Icon"></i>
    </div>
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
  right: 14px;
  bottom: 14px;
  width: 32px;
  height: 32px;
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
