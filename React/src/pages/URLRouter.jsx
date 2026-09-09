import { useState } from 'react'



function CreateURL() {
  const [formData, setFormData] = useState({
    url: "",
    alias: "",
    expires_at: ""
  });
  const [ URLData , setURLdata]= useState('')  
   const handleChange =(e) =>{
    const {name , value} = e.target
    
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
   } 
   const Genrate = async(e) =>{
      e.preventDefault();
      console.log(formData);

      const response = await fetch("http://localhost:8000/url", {  method: "post",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)})
      const data = await response.json();
      setURLdata(data[0])
   } 
  
  return (
    <>
    <form onSubmit={Genrate}>
      
      <input type="url" name="url" value={formData.url} id="LongURL_field" placeholder='URL'  onChange={handleChange}/>
      <input type="text" id="CustomAlies" name="alias" value={formData.alias} placeholder='custom alies'  onChange={handleChange}/>
      <input type="date" name="expires_at" id="ExpiryDate" value={formData.expires_at}  onChange={handleChange}/>
      <button type='submit' >Genrate</button>

    </form>

    <textarea type="text" id="URLData" name="URLData" value={URLData} readonly/>
    </>
  )
}

export default CreateURL