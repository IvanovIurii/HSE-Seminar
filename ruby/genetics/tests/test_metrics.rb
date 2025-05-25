require "minitest/autorun"
require "rmagick"
require_relative "../metrics"
require_relative "../target_loader"

class TestMetrics < Minitest::Test
  def setup
    @path = File.expand_path("test_sample.png", __dir__)
  end

  def test_should_get_same_similarity
    img1 = img2 = load_target_image(@path)

    assert_equal manhattan_diff(img1, img2), 0
  end

  def test_should_get_diff_similarity
    path_diff = File.expand_path("diff_sample.png", __dir__)

    img1 = load_target_image(@path)
    img2 = load_target_image(path_diff)

    assert_equal manhattan_diff(img1, img2), 190784422
  end
end
