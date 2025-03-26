AVASCRIPT:   document.addEventListener("DOMContentLoaded", function () {
    // Grafico Traffico
    const trafficChartElement = document.getElementById("trafficChart");
    new Chart(trafficChartElement, {
        type: "line",
        data: {
            labels: ["00:00", "06:00", "12:00", "18:00", "24:00"],
            datasets: [
                {
                    label: "Traffico (%)",
                    data: [20, 40, 70, 50, 30],
                    borderColor: "#36a2eb",
                    backgroundColor: "rgba(54, 162, 235, 0.5)", // Sfondo leggermente colorato
                    fill: true,
                },
            ],
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        color: "#000"  // Colore del testo della legenda
                    }
                }
            },
            layout: {
                backgroundColor: "white",  // Sfondo bianco per il grafico
            }
        }
    });
  
    // Animazione di ingresso per la sidebar
    gsap.to(".sidebar", {
        opacity: 1,
        x: 0,
        duration: 1,
        ease: "power4.out",
    });
  
    // Animazione di ingresso per i grafici
    gsap.to(".chart-container", {
        opacity: 1,
        y: 0,
        duration: 1.5,
        stagger: 0.3,
        ease: "power4.out",
    });
  
    // Effetto hover sui grafici
    const charts = document.querySelectorAll('.chart-container');
    charts.forEach(chart => {
        chart.addEventListener('mouseenter', () => {
            gsap.to(chart, {scale: 1.1, duration: 0.3, ease: "power1.out"});
        });
        chart.addEventListener('mouseleave', () => {
            gsap.to(chart, {scale: 1, duration: 0.3, ease: "power1.in"});
        });
    });
  
    // Animazione titolo di benvenuto
    gsap.to(".welcome-message", { 
        opacity: 1, 
        y: 0, 
        duration: 1, 
        ease: "power2.out" 
    });
  
    gsap.to(".sidebar", { 
        opacity: 1, 
        x: 0, 
        duration: 1, 
        delay: 0.5, 
        ease: "power2.out" 
    });
  });

