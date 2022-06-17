<template lang="pug">
  .wave_header
    .wave_header_inner
      slot
    div.wave_waves_container
      svg.wave_waves(
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        viewBox="0 24 170 28"
        preserveAspectRatio="none"
        shape-rendering="auto"
        )
        defs
          path(id="wave-gentle" d="M-160 44c30 0 58-18 88-18s 58 18 88 18 58-18 88-18 58 18 88 18 v44h-360z")
        g.wave_parallax
          use(xlink:href="#wave-gentle" x="60" y="0" fill="rgba(255,255,255,0.7")
          use(xlink:href="#wave-gentle" x="60" y="3" fill="rgba(255,255,255,0.5)")
          use(xlink:href="#wave-gentle" x="60" y="5" fill="rgba(255,255,255,0.3)")
          use(xlink:href="#wave-gentle" x="60" y="7" fill="#fff")
</template>
<style lang="sass">
.wave_header
  position: relative
  text-align: center
  background: linear-gradient(60deg, rgba(84,58,183,1) 0%, rgba(0,172,193,1) 100%)
  color: white

  &_inner
    height: 20vh
    width: 100%
    margin: 0
    padding: 0
    display: flex
    justify-content: center
    align-items: center
    text-align: center

  .wave_waves
    position: relative
    width: 100%
    height: 15vh
    margin-bottom: -7px /*Fix for safari gap*/
    min-height: 100px
    max-height: 150px

    /* Animation */

    .wave_parallax > use
      animation: move-forever 25s cubic-bezier(.55,.5,.45,.5) infinite

    .wave_parallax > use:nth-child(1)
      animation-delay: -2s
      animation-duration: 7s

    .wave_parallax > use:nth-child(2)
      animation-delay: -3s
      animation-duration: 10s
    .wave_parallax > use:nth-child(3)
      animation-delay: -4s
      animation-duration: 13s

    .wave_parallax > use:nth-child(4)
      animation-delay: -5s
      animation-duration: 20s

    @keyframes move-forever
      0%
        transform: translate3d(-90px,0,0)
      100%
        transform: translate3d(85px,0,0)
</style>
