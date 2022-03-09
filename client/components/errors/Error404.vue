<template lang="pug">
  v-row
    v-col.ml-16
      v-img.my-15.mx-auto(
        v-if="$colorMode.preference === 'dark'"
        :src="require('~/static/img/error404Night.svg')"
        width="70%"
        )
      v-img.my-15.mx-auto(v-else :src="require('~/static/img/error404.svg')" width="70%")
</template>
