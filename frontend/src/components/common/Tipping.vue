<template>
  <v-container class="text-center tipping__container">
    <a
      href="https://ofuse.me/o?uid=39000"
      data-ofuse-id="39000"
      data-ofuse-text="主にサーバー運用費月4000円に使用します！これからももっとサービスを良くしていきたいので、応援して頂けたら嬉しいです！！！"
      target="_blank"
      rel="noopener noreferrer"
    >
      主にサーバー運用費月4000円に使用します！<br />これからももっとサービスを良くしていきたいので、応援して頂けたら嬉しいです！！！
      <v-btn
        block
        color="blue lighten-1"
        elevation="24"
        rounded
        outlined
        class="tipping__btn text-center"
      >
        支援する
      </v-btn>
    </a>
  </v-container>
</template>

<style scoped>
.tipping__btn {
  display: inline-block;
  word-break: break-all;
  padding: 2px 8px;
  text-transform: none !important;
  white-space: normal;
  max-width: calc(100% - 30px);
  height: inherit !important;
}

.tipping__container > a {
  color: darkblue;
}
</style>
