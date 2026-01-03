<template>
    <div class="container">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Country Name</th>
                    <th scope="col">Threshold</th>
                    <th scope="col">driver</th>
                    <th scope="col">year</th>
                    <th scope="col">Loss Area</th>
                    <th scope="col">Action</th>
                </tr>
            </thead>
            <tbody v-for="forest in forests" :key="forest.id">
                <tr class="table-secondary">
                    <td>{{ forest.id }}</td>
                    <td>{{ forest.country }}</td>
                    <td>{{ forest.threshold }}</td>
                    <td>{{ forest.driver }}</td>
                    <td>{{ forest.year }}</td>
                    <td>{{ forest.loss }}</td>
                    <td>
                        <a href="" class="btn btn-primary btn-sm mr-4">Edit</a>
                        <button class="btn btn-danger btn-sm">Delete</button>
                    </td>
                </tr>
            </tbody>
                
        </table>
    </div>
</template>

<script setup>
    import axios from 'axios';
    import { ref, onMounted } from 'vue';

    const apiUrl = 'http://127.0.0.1:8000/api/forest/';

    const forests = ref([]);

    const getForests = async () => {
        try{
            const response = await axios.get(apiUrl);
            // forests.value = response.data;
            console.log(response.data);
            forests.value = response.data;
        } catch (error) {
            console.error('Error fetching forests:', error);
        }
    }

    onMounted(() => {
        console.log('Fetching forests data...');
        getForests();
    });
</script>