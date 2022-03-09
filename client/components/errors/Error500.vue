<template lang="pug">
  v-row
    v-col.ml-16
      v-img.my-15.mx-auto(
        v-if="$colorMode.preference === 'dark'"
        :src="require('~/static/img/error500Night.svg')"
        width="70%"
        )
      v-img.my-n9.mx-auto(v-else :src="require('~/static/img/error500.svg')" width="85%")
</template>
