<template>
  <div v-html="prettyValue" />
</template>

<script lang="ts">
import Vue from "vue";
import * as Diff2Html from "diff2html";

export default Vue.extend({
  name: "Diff2Html",
  props: {
    value: {
      type: String,
      required: true
    }
  },
  computed: {
    prettyValue(): string {
      return Diff2Html.html(this.value);
    }
  }
});
</script>

<style scoped lang="scss">
@import "~diff2html/bundles/css/diff2html.min.css";

::v-deep {
  td,
  th {
    padding: revert !important;
  }
}
</style>
