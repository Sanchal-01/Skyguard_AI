from PIL import Image

def remove_black_background(input_path, output_path, threshold=30, softness=20):
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        r, g, b, a = item
        # Calculate brightness / max component
        brightness = max(r, g, b)

        if brightness < threshold:
            # Completely transparent
            newData.append((0, 0, 0, 0))
        elif brightness < threshold + softness:
            # Smooth feathering on edges
            factor = (brightness - threshold) / softness
            new_a = int(a * factor)
            newData.append((r, g, b, new_a))
        else:
            newData.append((r, g, b, a))

    img.putdata(newData)
    img.save(output_path, "PNG")
    print("Background removed successfully!")

if __name__ == "__main__":
    remove_black_background(
        "c:/Users/ranu gaurav/OneDrive/Desktop/SkyGuard/public/aws_weather_station.png",
        "c:/Users/ranu gaurav/OneDrive/Desktop/SkyGuard/public/aws_weather_station.png",
        threshold=25,
        softness=15
    )
