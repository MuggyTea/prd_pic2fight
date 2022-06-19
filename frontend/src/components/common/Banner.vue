<template>
    <v-card
        class="img__banner"
        single-line
        :block="true"
    >
    <v-img
        src="../../assets/Bunner_text.svg"
        aspect-ratio="16/9"
        max-height="160"
        contain
    >
    </v-img>
    </v-card>
</template>

<script>
export default {
  name: "Banner",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
h1 {
  font-weight: bold;
  font-size: 24px;
}
h2 {
  font-size: 18px;
}
.img__banner{
    // position: relative;
    background-color: rgb(231,224,206) !important;
}

.text__img{
    // background-color: rgba( 255, 255, 255, 0.55 );
    // position: absolute;
    top: 80%;
    left: 20%;
    // transform: translate(-50%, -50%);
    // font-weight: bold;
    // font-size: 4vmin;
}
</style>
