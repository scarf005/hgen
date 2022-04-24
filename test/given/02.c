void verLine(t_info*	info, int x, int y1, int y2, int color) {
  int y;

  y = y1;
  while (y <= y2) {
    mlx_pixel_put(info->mlx, info->win, x, y, color);
    y++;
  }
}

int main_loop(t_info* info) {
  calc(info);
  // mlx_put_image_to_window(info->mlx, info->win, &info->img, 0, 0);

  return (0);
}
