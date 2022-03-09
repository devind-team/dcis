<template lang="pug">
  v-row
    v-col(cols="12").text-center
      h1.my-5 {{ $t('error.title403') }}
      v-img.mx-auto(:src="require('~/static/img/error403.png')" width="70%")
      .caption {{ $t('error.text403') }}
</template>
