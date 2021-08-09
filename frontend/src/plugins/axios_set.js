import axios from "axios";

axios.defaults.baseURL = "https://aitter-twigene.me";
axios.defaults.headers.post["Content-Type"] = "application/json;charset=utf-8";
axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";

export default axios;
