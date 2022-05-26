<template lang="pug">
  v-row
    v-col.my-2.d-flex.align-center
      v-btn-toggle(multiple)
        v-btn(height="40")
          v-icon mdi-format-bold
        v-btn(height="40")
          v-icon mdi-format-italic
        v-btn(height="40")
          v-icon mdi-format-strikethrough
      v-select.mx-1.shrink(
        v-model="underline"
        :items="underlineValues"
        style="width: 75px"
        filled
        outlined
        hide-details
        dense
      )
        template(#selection)
        template(#prepend-inner)
          v-icon mdi-format-underline
      v-btn-toggle.mx-1
        v-btn(height="40")
          v-icon mdi-format-align-left
        v-btn(height="40")
          v-icon mdi-format-align-center
        v-btn(height="40")
          v-icon mdi-format-align-right
      v-btn-toggle.mx-1
        v-btn(height="40")
          v-icon mdi-format-align-top
        v-btn(height="40")
          v-icon mdi-format-align-middle
        v-btn(height="40")
          v-icon mdi-format-align-bottom
      v-combobox.mx-1.shrink(
        v-model="size"
        :label="t('dcis.grid.sheetToolbar.fontSize')"
        :items="sizes"
        style="width: 150px"
        filled
        outlined
        hide-details
        dense
      )
      v-combobox.ml-1.shrink(
        v-model="kind"
        :label="t('dcis.grid.sheetToolbar.kind')"
        :items="kinds"
        style="width: 150px"
        filled
        outlined
        hide-details
        dense
      )
</template>

<script lang="ts">
export default defineComponent({
  setup () {
    const { t } = useI18n()

    const underline = ref<string | null>(null)
    const underlineValues = [
      { text: t('dcis.grid.sheetToolbar.underlineValues.single'), value: 'single' },
      { text: t('dcis.grid.sheetToolbar.underlineValues.double'), value: 'double' },
      { text: t('dcis.grid.sheetToolbar.underlineValues.singleAccounting'), value: 'singleAccounting' },
      { text: t('dcis.grid.sheetToolbar.underlineValues.doubleAccounting'), value: 'doubleAccounting' }
    ]

    const size = ref<number | null>(null)
    const sizes = Array
      .from(new Array(19).keys())
      .map((e: number) => e + 6)
      .map((e: number) => ({ text: `${e}px`, value: e }))

    const kind = ref<string | null>(null)
    const kinds = computed<{ text: string, value: string }[]>(() => (
      Object.keys(cellKinds).map((k: string) => ({ text: t(`dcis.grid.cellKinds.${k}`) as string, value: k })))
    )

    return { t, underline, underlineValues, size, sizes, kind, kinds }
  }
})
</script>
