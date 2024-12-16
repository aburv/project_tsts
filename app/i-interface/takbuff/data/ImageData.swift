//
//  ImageData.swift
//  takbuff
//
//  Created by Gurunathan Ramalingam on 26/09/24.
//

import Foundation
import SwiftUI

class ImageData: ObservableObject {
    private static let NAMESPACE = "image/"
    
    private let data: ApiRequest = ApiRequest()
    private let cache: ImageCache = ImageCache()
    
    @Published var image: UIImage?
        
    init(imageId: String, size: String) {
        loadImage(imageId: imageId, size: size)
    }
    
    private func loadImage(imageId: String, size: String) {
        let urlString = ImageData.NAMESPACE +  imageId + "/" + size
        
        if let imageFromCache = ImageCache().get(from: urlString) {
            self.image = imageFromCache
            return
        }

        data.get(path: urlString){ data, error in
            guard let data = data else {
                return
            }
            DispatchQueue.main.async {
                guard let loadedImage = UIImage(data: data) else { return }
                self.image = loadedImage
                ImageCache().set(image: loadedImage, key: urlString)
            }
        }
    }
}
