import { useState } from "react";

function App() {
    const [file, setFile] = useState(null);
    const [imageSrc, setImageSrc] = useState(null);
    const [objectsInfo, setObjectsInfo] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setFile(file);
        }
    };

    const sendImage = async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        setIsLoading(true);
        setError(null);

        try {
            // Wysyłamy obrazek do serwera
            const response = await fetch("http://127.0.0.1:8000/detect", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Błąd podczas wysyłania obrazu");
            }

            // Odczytujemy dane JSON z odpowiedzi
            const data = await response.json();
            setObjectsInfo(data.objects_info);  // Zapisujemy wyniki detekcji

            // Odczytujemy obraz jako blob
            const imageBlob = await fetch("http://127.0.0.1:8000" + data.image);
            const imageBlobData = await imageBlob.blob();
            const imageUrl = URL.createObjectURL(imageBlobData);  // Tworzymy URL z obrazu
            setImageSrc(imageUrl);  // Ustawiamy wynikowy obraz
        } catch (error) {
            console.error("Wystąpił błąd:", error);
            setError("Wystąpił błąd podczas komunikacji z serwerem");
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = () => {
        if (file) {
            sendImage(file);
        }
    };

    return (
        <div className="container">
            <h1>Wykrywanie obiektów</h1>
            <p>Prześlij obrazek, aby wykryć obiekty.</p>

            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button onClick={handleSubmit} disabled={isLoading}>
                {isLoading ? "Ładowanie..." : "Prześlij obraz"}
            </button>

            {error && <p className="error">{error}</p>}

            {imageSrc && <img src={imageSrc} alt="Wynik detekcji" />}
            {objectsInfo.length > 0 && (
                <div>
                    <h3>Wykryte obiekty:</h3>
                    <ul>
                        {objectsInfo.map((obj, index) => (
                            <li key={index}>
                                {obj.label}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;
