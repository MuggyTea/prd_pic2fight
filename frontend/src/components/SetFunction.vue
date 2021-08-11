<template>
    <div>
    <photo-upload />
    <photo-form />
    </div>
</template>

<script>
import PhotoUpload from "./PhotoUpload"
import PhotoFrom from "./PhotoForm"
export default {
    name: "Function",
    data () {
        return {
            "uploaded-photo": false
        }
    },
    components: {
        "photo-form": PhotoFrom,
        "photo-upload": PhotoUpload
    }
}
</script>
