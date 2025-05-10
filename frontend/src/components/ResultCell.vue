<template>
  <td :class="css_class">
    {{ entry_input[field] }}
  </td>
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'ResultCell',
  props: {
    entry_input: Object,
    entry_output: Object,
    field: String,
  },
  setup(props) {
    const css_class = ref('');
    const hash_field = props.field.concat('_hash');

    if (props.entry_output[hash_field]) css_class.value = 'table-success';
    else css_class.value = 'table-danger';

    return {
      css_class: css_class,
    };
  },
});
</script>
