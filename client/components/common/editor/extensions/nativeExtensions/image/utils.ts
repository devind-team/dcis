type ImageResult = {
  width: number
  height: number
}

interface ImageCache {
  [key: string]: ImageResult
}

const IMAGE_CACHE: ImageCache = {}

export function resolveImg (src: string): Promise<ImageResult> {
  return new Promise<ImageResult>((resolve, reject) => {
    if (src in IMAGE_CACHE) {
      resolve(IMAGE_CACHE[src])
      return
    }
    const img = new Image()
    const result: ImageResult = { width: 100, height: 1000 }

    img.onload = () => {
      result.width = img.width
      result.height = img.height
      IMAGE_CACHE[src] = result
      resolve(result)
    }
    img.onerror = () => reject(result)
    img.src = src
  })
}
