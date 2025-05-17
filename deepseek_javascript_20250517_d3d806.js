<script>
    document.getElementById('priceForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculating...';
        
        // Collect form data
        const formData = {
            location: document.getElementById('location').value,
            bedrooms: document.getElementById('bedrooms').value,
            bathrooms: document.getElementById('bathrooms').value,
            sqft: document.getElementById('sqft').value,
            year: document.getElementById('year').value,
            condition: document.getElementById('condition').value
        };
        
        try {
            // Send to backend
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Display the result
                document.getElementById('predictedPrice').textContent = 
                    data.predicted_price.toLocaleString();
                document.getElementById('results').style.display = 'block';
                
                // Scroll to results
                document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
            } else {
                alert('Error: ' + (data.error || 'Unknown error occurred'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the prediction service');
        } finally {
            // Reset button
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calculate Price';
        }
    });
</script>